from collections import OrderedDict
import pathlib

import attr
import lingpy
from clldutils.misc import slug
from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.forms import FormSpec
from pylexibank.util import progressbar

@attr.s
class CustomLanguage(Language):
    Country = attr.ib(default=None)
    Name_in_Source = attr.ib(default=None)

class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "clarkkimmun"
    language_class = CustomLanguage
    form_spec = FormSpec(
        missing_data=['', '-------'],
        separators=";/,",
        brackets={'(': ')', '[': ']'},
        strip_inside_brackets=True,
        first_form_only=True
    )

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.

        >>> args.writer.objects['LanguageTable'].append(...)
        """
        # add source
        args.writer.add_sources()
        # read in data
        mergedfile = self.raw_dir / 'KimMun_merged.tsv'
        wl = lingpy.Wordlist(mergedfile.as_posix())
        # add languages
        languages = {}
        for lang in self.languages:
            #print(lang)
            args.writer.add_language(
                 ID = lang['ID'],
                 Name = lang['Name'],
                 Latitude = lang['Latitude'],
                 Longitude = lang['Longitude']
             )
            languages[lang['Name']]=lang['ID']
        # make concept dictionary
        concepts = {}
        for concept in self.concepts:
            idx = concept['ID']+'_'+slug(concept['GLOSS'])
            args.writer.add_concept(
                ID=idx,
                Name=concept['GLOSS'],
                Concepticon_Gloss=concept['CONCEPTICON_GLOSS'],
                Concepticon_ID=concept['CONCEPTICON_ID']
                )
            concepts[concept['GLOSS']]=idx
        # create forms
        for idx in progressbar(wl, desc = 'cldfify the data'):
            cogid = idx
            if wl[idx, "concept"]:
                for lex in args.writer.add_forms_from_value(
                    Language_ID=languages[wl[idx, "doculect"]],
                    Parameter_ID=concepts[wl[idx, "concept"]],
                    Value=wl[idx, "ipa"]
                  ):
            # # add cognate
                    args.writer.add_cognate(
                        lexeme=lex,
                        Cognateset_ID = cogid
                        )
