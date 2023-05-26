from codemodder.__main__ import run
from codemodder.cli import parse_args


class TestExitCode:
    def test_success_0(self):
        run(
            parse_args(
                [
                    "tests/samples/",
                    "--output",
                    "here.txt",
                    "--codemod=url-sandbox",
                    "--path-exclude",
                    "*request.py",
                ]
            )
        )

    def test_bad_project_dir_1(self):
        exit_code = run(
            parse_args(
                [
                    "bad/path/",
                    "--output",
                    "here.txt",
                    "--codemod=url-sandbox",
                ]
            )
        )
        assert exit_code == 1
