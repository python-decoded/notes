from typing import Iterable
from youtube_client import YoutubeClient
from sentiments_classifier import SentimentsClassifier
from excel_utils import save_to_excel_file


class EtlSource:

    def read_rows(self) -> Iterable[dict]:
        yield from []


class YoutubeCommentsSource(EtlSource):

    def __init__(self, video_id: str):
        self.youtube_client = YoutubeClient()
        self.video_id = video_id

    def read_rows(self) -> Iterable[dict]:
        for comment in self.youtube_client.get_comments(self.video_id):
            yield comment.model_dump()


class EtlProcessor:

    def process_row(self, row: dict):
        return row


class SentimentsProcessor(EtlProcessor):

    def __init__(self, text_field: str):
        self.classifier = SentimentsClassifier()
        self.text_field = text_field

    def process_row(self, row: dict):
        row = row.copy()
        res = self.classifier.classify(row.get(self.text_field, ""))
        row.update(res)
        return row


class EtlTarget:

    def write_rows(self, rows: Iterable[dict]):
        pass


class ExcelTarget(EtlTarget):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def write_rows(self, rows: Iterable[dict]):
        save_to_excel_file(rows, self.file_path)


class EtlPipeline:

    def __init__(
            self,
            source: EtlSource,
            processors: list[EtlProcessor],
            target: EtlTarget):

        self.source = source
        self.processors = processors
        self.target = target

    def run(self):

        rows = self.source.read_rows()

        for processor in self.processors:
            rows = (processor.process_row(row) for row in rows)

        self.target.write_rows(rows)


if __name__ == "__main__":
    source = YoutubeCommentsSource("zZis75sAdPg")
    processor = SentimentsProcessor("textDisplay")
    target = ExcelTarget("test_etl.xlsx")
    etl = EtlPipeline(source, [processor], target)
    etl.run()
