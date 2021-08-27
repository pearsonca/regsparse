
stopifnot(require(data.table))

.debug <- "."
.args <- if (interactive()) file.path(
  .debug[1],
  c("digests", "summary.csv")
) else commandArgs(trailingOnly = TRUE)

fl <- list.files(.args[1], pattern = "csv$", full.names = TRUE)

alldigests <- rbindlist(lapply(fl, function(fl) fread(fl)[, doc := gsub("^.*/([^\\.]+)\\.csv$","\\1", fl)]))
names(alldigests)[c(3,5)] <- c("kcount", "acount")

res <- alldigests[, .(phrasecount = sum(kcount), acronymcount = sum(acount)), by=.(doc, keyphrase, acronym)]

fwrite(res, tail(.args, 1))