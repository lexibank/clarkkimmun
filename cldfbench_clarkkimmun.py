from collections import OrderedDict
import pathlib

import attr
import lingpy
from clldutils.misc import slug
from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as MyDataset
from pylexibank.forms import FormSpec
from pylexibank.util import progressbar

@attr.s
class CustomConcept(Concept):
    Gloss_in_Source = attr.ib(default=None)
    Doculect = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    Family = attr.ib(default="Hmong-Mien")
    Country = attr.ib(default=None)
    Name_in_Source = attr.ib(default=None)
    ISO = attr.ib(default='mji')

class Dataset(MyDataset):
    dir = pathlib.Path(__file__).parent
    id = "clarkkimmun"
    language_class = CustomLanguage
    concept_class = CustomConcept
    form_spec = FormSpec(
        missing_data=['', '-------'],
        separators=";/,",
        brackets={'(': ')', '[': ']'},
        strip_inside_brackets=True,
        first_form_only=True
    )

    def cldf_specs(self):  # A dataset must declare all CLDF sets it creates.
        return super().cldf_specs()

    def cmd_download(self, args):
        """
        Download files to the raw/ directory. You can use helpers methods of `self.raw_dir`, e.g.

        >>> self.raw_dir.download(url, fname)
        """
        pass

    def cmd_makecldf(self, args):
        """
        Convert the raw data to a CLDF dataset.

        >>> args.writer.objects['LanguageTable'].append(...)
        """
        # add source
        args.writer.add_sources()
        # read in raw data, Laos and Vietnam
        Laos = self.raw_dir.read_csv("KimMun_Laos.tsv",
                dicts=True,
                delimiter="\t")
        Vietnam = self.raw_dir.read_csv("KimMun_Vietnam.tsv",
                dicts=True,
                delimiter="\t")
        #combine data
        Data={0:['ID',
                'concept',
                'doculect',
                'ipa']}
        i = 1
        for each in Laos:
            Data[i] = ['Laos_'+each['ID'],
                        each['English'],
                        'Luang Nam Tha, Laos',
                        each['Luang Nam Tha, Laos']]
            i = i + 1
        v = len(Data)
        for each in Vietnam:
            Data[v] = ['Vietnam_'+each['ID'],
                       each['English'],
                       'Lao Cai, Vietnam',
                       each['Lao Cai, Vietnam']]
            v = v +1
        #print(Data)
        wl = lingpy.Wordlist(Data)
        for idx, val in wl.iter_rows('ipa'):
            print(idx, wl[idx])
        languages = {}
        for lang in self.languages:
            print(lang)
            args.writer.add_language(
                 ID = lang['ID'],
                 Name = lang['Name'],
                 Latitude = lang['Latitude'],
                 Longitude = lang['Longitude']
             )
            languages[lang['Name']]=lang['ID']
        print(languages)
        # make concept dictionary
        concepts = {}
        for concept in self.concepts:
            idx = concept['ID']+'_'+slug(concept['GLOSS'])
            args.writer.add_concept(
                ID=idx,
                Name=concept['GLOSS'])
            concepts[concept['GLOSS']]=idx
        print(concepts)
        # create forms
        for idx in progressbar(wl, desc = 'cldfify the data'):
            cogid = idx
            if wl[idx, "ipa"]:
                #print(idx,wl[idx])
                lex=args.writer.add_forms_from_value(
                     Language_ID=languages[wl[idx, "doculect"]],
                     Parameter_ID=wl[idx, "concept"],
                     Value=wl[idx, "ipa"]
                 )
            # add cognate
                args.writer.add_cognate(
                     lexeme=lex,
                     Cognateset_ID = cogid
                 )
