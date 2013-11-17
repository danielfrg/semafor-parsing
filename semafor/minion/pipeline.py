# encoding: utf-8
import os
import nltk
import luigi
import fnmatch
import subprocess


DATA_DIR = '/Users/danielfrg/Documents/semafor/distribution/minion/data'
SEMAFOR_DIR = '/Users/danielfrg/Documents/semafor/semafor'


class InputText(luigi.ExternalTask):

    def output(self):
        files = os.listdir(DATA_DIR)
        inputs = fnmatch.filter(files, '*.txt')
        return [luigi.LocalTarget(os.path.join(DATA_DIR, fname)) for fname in inputs]


class SentenceTockenize(luigi.Task):

    def requires(self):
        return InputText()

    def output(self):
        files = os.listdir(DATA_DIR)
        outputs = fnmatch.filter(files, '*.txt')
        # Remove .txt and add .tockenized
        outputs = [f[:-4] + '.tockenized' for f in outputs]
        return [luigi.LocalTarget(os.path.join(DATA_DIR, fname)) for fname in outputs]

    def run(self):
        for infile, outfile in zip(self.input(), self.output()):
            infile = infile.open('r')
            document = infile.read().decode('utf-8')

            sentences = nltk.tokenize.sent_tokenize(document)
            sentences = [unicode(sentence).replace('\n', ' ') for sentence in sentences]

            f = outfile.open('w')
            f.write('\n'.join(sentences).encode('utf-8'))
            f.close()


class SemaforParsing(luigi.Task):

    def requires(self):
        return SentenceTockenize()

    def output(self):
        files = os.listdir(DATA_DIR)
        outputs = fnmatch.filter(files, '*.tockenized')
        # Remove .tockenized and add .json
        outputs = [f[:-11] + '.json' for f in outputs]
        return [luigi.LocalTarget(os.path.join(DATA_DIR, fname)) for fname in outputs]

    def run(self):
        for infile, outfile in zip(self.input(), self.output()):
            infile = infile.path
            outfile = outfile.path

            runSemafor = os.path.join(SEMAFOR_DIR, 'bin', 'runSemafor.sh')
            call = [runSemafor, os.path.abspath(infile), os.path.abspath(outfile), '1']
            subprocess.call(call)

if __name__ == '__main__':
    luigi.run(main_task_cls=SemaforParsing)
