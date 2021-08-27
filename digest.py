import sys # for getting CL arguments
import pandas as pd # for data manipulation; TODO factor out? big dependency
import PyPDF2 # for parsing PDFs
import re # for regular expression work

# grab the command line arguments
# TODO refactor with argparse, including verbosity
dictfile, refpdf, outfile = sys.argv[1:]
verbose = 0

if verbose:
    print('Using dictionary: {}'.format(dictfile))
    print('On file: {}'.format(refpdf))
    print('Writing results to: {}'.format(outfile))

df = pd.read_csv(dictfile, dtype = str, na_values = [])
df.fillna('', inplace = True)

if verbose:
    print('Dictionary:')
    print(df)

# open the pdf file
sourcetext = PyPDF2.PdfFileReader(refpdf)

# get number of pages
pagerange = range(0, sourcetext.getNumPages())

def extractor(entries, pages):
    for page in pages:
        if verbose > 1:
            print("visiting page {}".format(page))
        txt = sourcetext.getPage(page).extractText()
        for entry in entries.itertuples():
            if verbose > 1:
                print("searching entry {}".format(entry.Index))
            kpn = len(re.findall(entry.keyphrase, txt, re.IGNORECASE))
            acn = 0 if entry.acronym == '' else len(re.findall(entry.acronym, txt))
            if (kpn + acn) > 0:
                yield (page, entry.keyphrase, kpn, entry.acronym, acn)

result = pd.DataFrame(
[res for res in extractor(df, pagerange)],
columns = ['page', 'keyphrase', 'count', 'acronym', 'count']
)

result.to_csv(outfile, index = False)
