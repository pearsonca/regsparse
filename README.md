# OVERVIEW

Performs dictionary-based summary of PDFs.

# USAGE

To use this tool, you will need the following parts: `Python3`, `R`, and `(gnu) make`, with library support as `pandas`, `PyPDF2`, `selenium`, and `BeautifulSoup` (`python`) and `data.table` (`R`), as well as the Chrome browser (for the `selenium` code). With those in place, the following steps will provide the digests and summary.

```
$ make setup
$ make countall
$ make summary
```

which gets some input and dependencies (`setup`), processes it (`countall`), and then summarizes (`summary`).

# EXTENSIBILITY

Some of these dependencies are likely modularly replaceable, _e.g._ the chrome-based selenium element could instead by a firefox-based version, and indeed that entirely section of the code is to pull an example corpus of instructions to evaluate.

The necessary `dictionary.csv` file is an example only, but of course an alternative set of search phrases could (should, even) be used.

The resulting summarization (via `summarize.R`) is one of many potentially interesting summaries; others could be added as desired.
