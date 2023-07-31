from typing import Any, Tuple
from libcst.codemod import ContextAwareVisitor, VisitorBasedCodemodCommand
from libcst.metadata import PositionProvider


class BaseTransformer(VisitorBasedCodemodCommand):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self, context, results, line_exclude=None, line_include=None):
        super().__init__(context)
        self.results = results
        self.line_exclude = line_exclude or []
        self.line_include = line_include or []

    def filter_by_result(self, pos_to_match):
        all_pos = [extract_pos_from_result(result) for result in self.results]
        return any(match_pos(pos_to_match, position) for position in all_pos)

    def filter_by_path_includes_or_excludes(self, pos_to_match):
        """
        Returns True if the node, whose position in the file is pos_to_match, matches any of the lines specified in the path-includes or path-excludes flags.
        """
        # excludes takes precedence if defined
        if self.line_exclude:
            return not any(match_line(pos_to_match, line) for line in self.line_exclude)
        if self.line_include:
            return any(match_line(pos_to_match, line) for line in self.line_include)
        return True


class BaseVisitor(ContextAwareVisitor):
    METADATA_DEPENDENCIES: Tuple[Any, ...] = (PositionProvider,)

    def __init__(self, context, results, line_exclude=None, line_include=None):
        super().__init__(context)
        self.results = results
        self.line_exclude = line_exclude or []
        self.line_include = line_include or []

    def filter_by_result(self, pos_to_match):
        all_pos = [extract_pos_from_result(result) for result in self.results]
        return any(match_pos(pos_to_match, position) for position in all_pos)

    def filter_by_path_includes_or_excludes(self, pos_to_match):
        """
        Returns True if the node, whose position in the file is pos_to_match, matches any of the lines specified in the path-includes or path-excludes flags.
        """
        # excludes takes precedence if defined
        if self.line_exclude:
            return not any(match_line(pos_to_match, line) for line in self.line_exclude)
        if self.line_include:
            return any(match_line(pos_to_match, line) for line in self.line_include)
        return True


def match_line(pos, line):
    return pos.start.line == line and pos.end.line == line


def extract_pos_from_result(result):
    region = result["locations"][0]["physicalLocation"]["region"]
    # TODO it may be the case some of these attributes do not exist
    return (
        region.get("startLine"),
        region["startColumn"],
        region.get("endLine") or region.get("startLine"),
        region["endColumn"],
    )


def match_pos(pos, x):
    # needs some leeway because the semgrep and libcst won't exactly match
    return (
        pos.start.line == x[0]
        and (pos.start.column in (x[1] - 1, x[1]))
        and pos.end.line == x[2]
        and (pos.end.column in (x[3] - 1, x[3]))
    )
