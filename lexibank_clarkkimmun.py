from collections import OrderedDict
import pathlib
import re
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
        missing_data=[''],
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
        languages = args.writer.add_languages(lookup_factory="Name")
        languages_dict = {}
        for lang in self.languages:
            languages_dict[lang['Name']]=lang['ID']
        concepts_dict = {}
        for conceptlist in self.conceptlists:
            for concept in conceptlist.concepts.values():
                args.writer.add_concept(ID="%s_%s" % (concept.number, slug(concept.english)),
                Name=concept.english,
                Concepticon_ID=concept.concepticon_id,
                Concepticon_Gloss=concept.concepticon_gloss
                )
                idx=concept.number+'_'+slug(concept.english)
                concepts_dict[concept.english]=idx
        # add lexemes
        for idx in progressbar(wl, desc = 'cldfify the data'):
            cogid = idx
            if not re.search('[ -]', wl[idx, "ipa"]):
                if wl[idx, "concept"]:
                    for lex in args.writer.add_forms_from_value(
                        Language_ID=languages_dict[wl[idx, "doculect"]],
                        Parameter_ID=concepts_dict[wl[idx, "concept"]],
                        Value=wl[idx, "ipa"],
                        Source='Clark2008'
                      ):
                # # add cognate
                        args.writer.add_cognate(
                            lexeme=lex,
                            Cognateset_ID = cogid
                            )
