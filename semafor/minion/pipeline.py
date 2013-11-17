# encoding: utf-8
import os
import nltk
import luigi
import requests
import settings
import subprocess
from bs4 import BeautifulSoup

# Just because luigi on Pypi does not have this class yet
from semafor.minion import s3


class InputTask(luigi.ExternalTask):

    def output(self):
        fin = os.path.join(settings.DATA_DIR, settings.URLS_FILE)
        return luigi.LocalTarget(fin)


class DownloadDocs(luigi.Task):

    def requires(self):
        return InputTask()

    def output(self):
        urls = self.input().open('r').read().split('\n')
        urls = [url[7:] if url.startswith('http://') else url for url in urls]
        urls = [url.replace('/', '|') for url in urls]
        urls = [url + '.txt' for url in urls]
        return [luigi.LocalTarget(os.path.join(settings.DATA_DIR, fname)) for fname in urls]

    def run(self):
        urls = self.input().open('r').read().split('\n')

        BASE_URL = 'http://readability.com/api/content/v1/parser'
        for url, outfile in zip(urls, self.output()):
            payload = {'url': url, 'token': settings.READABILITY_TOKEN}
            r = requests.get(BASE_URL, params=payload)
            html_content = r.json()['content']
            soup = BeautifulSoup(html_content)

            f = outfile.open('w')
            f.write(soup.get_text(' ').encode('utf-8'))
            f.close()


class SentenceTockenize(luigi.Task):

    def requires(self):
        return DownloadDocs()

    def output(self):
        files = self.input()
        files = [file.path for file in files]
        # Remove .txt and add .tockenized
        files = [f[:-4] + '.tockenized' for f in files]
        return [luigi.LocalTarget(os.path.join(settings.DATA_DIR, fname)) for fname in files]

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
        files = self.input()
        files = [file.path for file in files]
        # Remove .tockenized and add .json
        files = [f[:-11] + '.json' for f in files]
        return [luigi.LocalTarget(os.path.join(settings.DATA_DIR, fname)) for fname in files]

    def run(self):
        for infile, outfile in zip(self.input(), self.output()):
            infile = infile.path
            outfile = outfile.path

            runSemafor = os.path.join(settings.SEMAFOR_DIR, 'bin', 'runSemafor.sh')
            call = [runSemafor, os.path.abspath(infile), os.path.abspath(outfile), '1']
            subprocess.call(call)


class CopyToS3(luigi.Task):

    def requires(self):
        return SemaforParsing()

    def output(self):
        files = self.input()
        files = [file.path for file in files]
        # Get only filename
        files = [os.path.basename(fname) for fname in files]
        s3_client = s3.S3Client(aws_access_key_id=settings.AWS_KEY,
                                aws_secret_access_key=settings.AWS_SECRET)

        return [s3.S3Target(os.path.join(settings.S3_PATH, fname), client=s3_client) for fname in files]

    def run(self):
        for infile, outfile in zip(self.input(), self.output()):
            infile = infile.open('r')
            f = outfile.open('w')
            f.write(infile.read().decode('utf-8').encode('utf-8'))
            f.close()

if __name__ == '__main__':
    # luigi.run(main_task_cls=DownloadDocs, cmdline_args=['--local-scheduler'])
    luigi.run(main_task_cls=CopyToS3, cmdline_args=['--local-scheduler'])
