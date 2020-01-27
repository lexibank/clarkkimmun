from collections import OrderedDict
import pathlib

import attr
from clldutils.misc import slug
from pylexibank import Concept, Language
from pylexibank.dataset import Dataset as MyDataset
from pylexibank.forms import FormSpec
from pylexibank.util import progressbar

@attr.s
class CustomConcept(Concept):
    Gloss_in_Source = attr.ib(default=None)

@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    Family = attr.ib(default="Hmong-Mien")
    DataSource = attr.ib(default=None)
    Name_in_Source = attr.ib(default=None)
    Location = attr.ib(default=None)



class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "clarkkimmun"

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
