# This top-level module imports all public names from the package,
# and exposes them as public objects. We have tests to make sure
# no object is forgotten in this list.

"""Griffe package.

Signatures for entire Python programs.
Extract the structure, the frame, the skeleton of your project,
to generate API documentation or find breaking changes in your API.

The entirety of the public API is exposed here, in the top-level `griffe` module.

All messages written to standard output or error are logged using the `logging` module.
Our logger's name is set to `"griffe"` and is public (you can rely on it).
You can obtain the logger from the standard `logging` module: `logging.getLogger("griffe")`.

If you need to alter our logger, do so temporarily and restore it to its original state,
for example using [context managers][contextlib.contextmanager].
Actual logging messages are not part of the public API (they might change without notice).

Raised exceptions throughout the package are part of the public API (you can rely on them).
Their actual messages are not part of the public API (they might change without notice).
"""

from __future__ import annotations

from typing import Any

from _griffe.agents.inspector import Inspector, inspect
from _griffe.agents.nodes.assignments import get_instance_names, get_name, get_names
from _griffe.agents.nodes.ast import (
    ast_children,
    ast_first_child,
    ast_kind,
    ast_last_child,
    ast_next,
    ast_next_siblings,
    ast_previous,
    ast_previous_siblings,
    ast_siblings,
)
from _griffe.agents.nodes.docstrings import get_docstring
from _griffe.agents.nodes.exports import ExportedName, get__all__, safe_get__all__
from _griffe.agents.nodes.imports import relative_to_absolute
from _griffe.agents.nodes.parameters import ParametersType, get_parameters
from _griffe.agents.nodes.runtime import ObjectNode
from _griffe.agents.nodes.values import get_value, safe_get_value
from _griffe.agents.visitor import Visitor, builtin_decorators, stdlib_decorators, typing_overload, visit
from _griffe.c3linear import c3linear_merge
from _griffe.cli import DEFAULT_LOG_LEVEL, check, dump, get_parser, main
from _griffe.collections import LinesCollection, ModulesCollection
from _griffe.diff import (
    AttributeChangedTypeBreakage,
    AttributeChangedValueBreakage,
    Breakage,
    ClassRemovedBaseBreakage,
    ObjectChangedKindBreakage,
    ObjectRemovedBreakage,
    ParameterAddedRequiredBreakage,
    ParameterChangedDefaultBreakage,
    ParameterChangedKindBreakage,
    ParameterChangedRequiredBreakage,
    ParameterMovedBreakage,
    ParameterRemovedBreakage,
    ReturnChangedTypeBreakage,
    find_breaking_changes,
)
from _griffe.docstrings.google import parse_google
from _griffe.docstrings.models import (
    DocstringAdmonition,
    DocstringAttribute,
    DocstringClass,
    DocstringDeprecated,
    DocstringElement,
    DocstringFunction,
    DocstringModule,
    DocstringNamedElement,
    DocstringParameter,
    DocstringRaise,
    DocstringReceive,
    DocstringReturn,
    DocstringSection,
    DocstringSectionAdmonition,
    DocstringSectionAttributes,
    DocstringSectionClasses,
    DocstringSectionDeprecated,
    DocstringSectionExamples,
    DocstringSectionFunctions,
    DocstringSectionModules,
    DocstringSectionOtherParameters,
    DocstringSectionParameters,
    DocstringSectionRaises,
    DocstringSectionReceives,
    DocstringSectionReturns,
    DocstringSectionText,
    DocstringSectionWarns,
    DocstringSectionYields,
    DocstringWarn,
    DocstringYield,
)
from _griffe.docstrings.numpy import parse_numpy
from _griffe.docstrings.parsers import (
    DocstringDetectionMethod,
    DocstringStyle,
    infer_docstring_style,
    parse,
    parse_auto,
    parsers,
)
from _griffe.docstrings.sphinx import parse_sphinx
from _griffe.docstrings.utils import docstring_warning, parse_docstring_annotation
from _griffe.encoders import JSONEncoder, json_decoder
from _griffe.enumerations import (
    BreakageKind,
    DocstringSectionKind,
    ExplanationStyle,
    Kind,
    LogLevel,
    ObjectKind,
    ParameterKind,
    Parser,
)
from _griffe.exceptions import (
    AliasResolutionError,
    BuiltinModuleError,
    CyclicAliasError,
    ExtensionError,
    ExtensionNotLoadedError,
    GitError,
    GriffeError,
    LastNodeError,
    LoadingError,
    NameResolutionError,
    RootNodeError,
    UnhandledEditableModuleError,
    UnimportableModuleError,
)
from _griffe.expressions import (
    Expr,
    ExprAttribute,
    ExprBinOp,
    ExprBoolOp,
    ExprCall,
    ExprCompare,
    ExprComprehension,
    ExprConstant,
    ExprDict,
    ExprDictComp,
    ExprExtSlice,
    ExprFormatted,
    ExprGeneratorExp,
    ExprIfExp,
    ExprJoinedStr,
    ExprKeyword,
    ExprLambda,
    ExprList,
    ExprListComp,
    ExprName,
    ExprNamedExpr,
    ExprParameter,
    ExprSet,
    ExprSetComp,
    ExprSlice,
    ExprSubscript,
    ExprTuple,
    ExprUnaryOp,
    ExprVarKeyword,
    ExprVarPositional,
    ExprYield,
    ExprYieldFrom,
    get_annotation,
    get_base_class,
    get_condition,
    get_expression,
    safe_get_annotation,
    safe_get_base_class,
    safe_get_condition,
    safe_get_expression,
)
from _griffe.extensions.base import (
    Extension,
    Extensions,
    LoadableExtensionType,
    builtin_extensions,
    load_extensions,
)
from _griffe.extensions.dataclasses import DataclassesExtension
from _griffe.finder import ModuleFinder, NamePartsAndPathType, NamePartsType, NamespacePackage, Package
from _griffe.git import assert_git_repo, get_latest_tag, get_repo_root, tmp_worktree
from _griffe.importer import dynamic_import, sys_path
from _griffe.loader import GriffeLoader, load, load_git, load_pypi
from _griffe.logger import Logger, get_logger, logger, patch_loggers
from _griffe.merger import merge_stubs
from _griffe.mixins import (
    DelMembersMixin,
    GetMembersMixin,
    ObjectAliasMixin,
    SerializationMixin,
    SetMembersMixin,
)
from _griffe.models import (
    Alias,
    Attribute,
    Class,
    Decorator,
    Docstring,
    Function,
    Module,
    Object,
    Parameter,
    Parameters,
)
from _griffe.stats import Stats
from _griffe.tests import (
    TmpPackage,
    htree,
    module_vtree,
    temporary_inspected_module,
    temporary_inspected_package,
    temporary_pyfile,
    temporary_pypackage,
    temporary_visited_module,
    temporary_visited_package,
    vtree,
)

# Regenerate this list with the following Python snippet:
# import griffe
# names = sorted(n for n in dir(griffe) if not n.startswith("_") and n not in ("annotations", "Any"))
# print('__all__ = [\n    "' + '",\n    "'.join(names) + '",\n]')
__all__ = [
    "Alias",
    "AliasResolutionError",
    "Attribute",
    "AttributeChangedTypeBreakage",
    "AttributeChangedValueBreakage",
    "Breakage",
    "BreakageKind",
    "BuiltinModuleError",
    "Class",
    "ClassRemovedBaseBreakage",
    "CyclicAliasError",
    "DEFAULT_LOG_LEVEL",
    "DataclassesExtension",
    "Decorator",
    "DelMembersMixin",
    "Docstring",
    "DocstringAdmonition",
    "DocstringAttribute",
    "DocstringClass",
    "DocstringDeprecated",
    "DocstringDetectionMethod",
    "DocstringElement",
    "DocstringFunction",
    "DocstringModule",
    "DocstringNamedElement",
    "DocstringParameter",
    "DocstringRaise",
    "DocstringReceive",
    "DocstringReturn",
    "DocstringSection",
    "DocstringSectionAdmonition",
    "DocstringSectionAttributes",
    "DocstringSectionClasses",
    "DocstringSectionDeprecated",
    "DocstringSectionExamples",
    "DocstringSectionFunctions",
    "DocstringSectionKind",
    "DocstringSectionModules",
    "DocstringSectionOtherParameters",
    "DocstringSectionParameters",
    "DocstringSectionRaises",
    "DocstringSectionReceives",
    "DocstringSectionReturns",
    "DocstringSectionText",
    "DocstringSectionWarns",
    "DocstringSectionYields",
    "DocstringStyle",
    "DocstringWarn",
    "DocstringYield",
    "ExplanationStyle",
    "ExportedName",
    "Expr",
    "ExprAttribute",
    "ExprBinOp",
    "ExprBoolOp",
    "ExprCall",
    "ExprCompare",
    "ExprComprehension",
    "ExprConstant",
    "ExprDict",
    "ExprDictComp",
    "ExprExtSlice",
    "ExprFormatted",
    "ExprGeneratorExp",
    "ExprIfExp",
    "ExprJoinedStr",
    "ExprKeyword",
    "ExprLambda",
    "ExprList",
    "ExprListComp",
    "ExprName",
    "ExprNamedExpr",
    "ExprParameter",
    "ExprSet",
    "ExprSetComp",
    "ExprSlice",
    "ExprSubscript",
    "ExprTuple",
    "ExprUnaryOp",
    "ExprVarKeyword",
    "ExprVarPositional",
    "ExprYield",
    "ExprYieldFrom",
    "Extension",
    "ExtensionError",
    "ExtensionNotLoadedError",
    "Extensions",
    "Function",
    "GetMembersMixin",
    "GitError",
    "GriffeError",
    "GriffeLoader",
    "Inspector",
    "JSONEncoder",
    "Kind",
    "LastNodeError",
    "LinesCollection",
    "LoadableExtensionType",
    "LoadingError",
    "Logger",
    "LogLevel",
    "Module",
    "ModuleFinder",
    "ModulesCollection",
    "NamePartsAndPathType",
    "NamePartsType",
    "NameResolutionError",
    "NamespacePackage",
    "Object",
    "ObjectAliasMixin",
    "ObjectChangedKindBreakage",
    "ObjectKind",
    "ObjectNode",
    "ObjectRemovedBreakage",
    "Package",
    "Parameter",
    "ParameterAddedRequiredBreakage",
    "ParameterChangedDefaultBreakage",
    "ParameterChangedKindBreakage",
    "ParameterChangedRequiredBreakage",
    "ParameterKind",
    "ParameterMovedBreakage",
    "ParameterRemovedBreakage",
    "Parameters",
    "ParametersType",
    "Parser",
    "ReturnChangedTypeBreakage",
    "RootNodeError",
    "SerializationMixin",
    "SetMembersMixin",
    "Stats",
    "TmpPackage",
    "UnhandledEditableModuleError",
    "UnimportableModuleError",
    "Visitor",
    "assert_git_repo",
    "ast_children",
    "ast_first_child",
    "ast_kind",
    "ast_last_child",
    "ast_next",
    "ast_next_siblings",
    "ast_previous",
    "ast_previous_siblings",
    "ast_siblings",
    "builtin_decorators",
    "builtin_extensions",
    "c3linear_merge",
    "check",
    "dump",
    "docstring_warning",
    "dynamic_import",
    "find_breaking_changes",
    "get__all__",
    "get_annotation",
    "get_base_class",
    "get_condition",
    "get_docstring",
    "get_expression",
    "get_instance_names",
    "get_latest_tag",
    "get_logger",
    "get_name",
    "get_names",
    "get_parameters",
    "get_parser",
    "get_repo_root",
    "get_value",
    "htree",
    "infer_docstring_style",
    "inspect",
    "json_decoder",
    "load",
    "load_extensions",
    "load_git",
    "load_pypi",
    "logger",
    "main",
    "merge_stubs",
    "module_vtree",
    "parse",
    "parse_auto",
    "parse_docstring_annotation",
    "parse_google",
    "parse_numpy",
    "parse_sphinx",
    "parsers",
    "patch_loggers",
    "relative_to_absolute",
    "safe_get__all__",
    "safe_get_annotation",
    "safe_get_base_class",
    "safe_get_condition",
    "safe_get_expression",
    "safe_get_value",
    "stdlib_decorators",
    "sys_path",
    "temporary_inspected_module",
    "temporary_inspected_package",
    "temporary_pyfile",
    "temporary_pypackage",
    "temporary_visited_module",
    "temporary_visited_package",
    "tmp_worktree",
    "typing_overload",
    "visit",
    "vtree",
]


class _APIScope:
    def __getattr__(self, name: str) -> Any:
        try:
            return globals()[name]
        except KeyError as error:
            raise AttributeError(f"module 'griffe' has no attribute {name!r}") from error


class _CLIScope(_APIScope):
    def __init__(self) -> None:
        self.main = main
        self.check = check
        self.dump = dump
        self.get_parser = get_parser


class _LoadersScope(_APIScope):
    def __init__(self) -> None:
        self.load = load
        self.load_git = load_git
        self.load_pypi = load_pypi
        self.GriffeLoader = GriffeLoader
        self.ModulesCollection = ModulesCollection
        self.LinesCollection = LinesCollection
        self.Stats = Stats
        self.merge_stubs = merge_stubs


class _FinderScope(_APIScope):
    def __init__(self) -> None:
        self.ModuleFinder = ModuleFinder
        self.Package = Package
        self.NamespacePackage = NamespacePackage
        self.NamePartsType = NamePartsType
        self.NamePartsAndPathType = NamePartsAndPathType


class _ModelsScope(_APIScope):
    def __init__(self) -> None:
        self.Module = Module
        self.Object = Object
        self.Class = Class
        self.Function = Function
        self.Parameter = Parameter
        self.Parameters = Parameters
        self.Alias = Alias
        self.Attribute = Attribute
        self.Decorator = Decorator
        self.Docstring = Docstring
        self.Kind = Kind
        self.GetMembersMixin = GetMembersMixin
        self.SetMembersMixin = SetMembersMixin
        self.DelMembersMixin = DelMembersMixin
        self.SerializationMixin = SerializationMixin
        self.ObjectAliasMixin = ObjectAliasMixin
        self.c3linear_merge = c3linear_merge
        self.ParameterKind = ParameterKind


class _AgentsScope(_APIScope):
    def __init__(self) -> None:
        self.Inspector = Inspector
        self.inspect = inspect
        self.Visitor = Visitor
        self.visit = visit
        self.builtin_decorators = builtin_decorators
        self.stdlib_decorators = stdlib_decorators
        self.typing_overload = typing_overload
        self.ast_children = ast_children
        self.ast_first_child = ast_first_child
        self.ast_last_child = ast_last_child
        self.ast_next = ast_next
        self.ast_previous = ast_previous
        self.ast_siblings = ast_siblings
        self.ast_next_siblings = ast_next_siblings
        self.ast_previous_siblings = ast_previous_siblings
        self.ast_kind = ast_kind
        self.get_name = get_name
        self.get_names = get_names
        self.get_instance_names = get_instance_names
        self.get_docstring = get_docstring
        self.get__all__ = get__all__
        self.safe_get__all__ = safe_get__all__
        self.get_parameters = get_parameters
        self.get_value = get_value
        self.safe_get_value = safe_get_value
        self.relative_to_absolute = relative_to_absolute


class _DocstringsScope(_APIScope):
    def __init__(self) -> None:
        self.DocstringStyle = DocstringStyle
        self.DocstringDetectionMethod = DocstringDetectionMethod
        self.DocstringSectionKind = DocstringSectionKind
        self.DocstringSection = DocstringSection
        self.DocstringSectionText = DocstringSectionText
        self.DocstringSectionParameters = DocstringSectionParameters
        self.DocstringSectionReturns = DocstringSectionReturns
        self.DocstringSectionReceives = DocstringSectionReceives
        self.DocstringSectionYields = DocstringSectionYields
        self.DocstringSectionRaises = DocstringSectionRaises
        self.DocstringSectionWarns = DocstringSectionWarns
        self.DocstringSectionExamples = DocstringSectionExamples
        self.DocstringSectionAttributes = DocstringSectionAttributes
        self.DocstringSectionClasses = DocstringSectionClasses
        self.DocstringSectionModules = DocstringSectionModules
        self.DocstringSectionFunctions = DocstringSectionFunctions
        self.DocstringSectionDeprecated = DocstringSectionDeprecated
        self.DocstringSectionAdmonition = DocstringSectionAdmonition
        self.DocstringElement = DocstringElement
        self.DocstringParameter = DocstringParameter
        self.DocstringReturn = DocstringReturn
        self.DocstringReceive = DocstringReceive
        self.DocstringYield = DocstringYield
        self.DocstringRaise = DocstringRaise
        self.DocstringWarn = DocstringWarn
        self.DocstringAdmonition = DocstringAdmonition
        self.DocstringAttribute = DocstringAttribute
        self.DocstringClass = DocstringClass
        self.DocstringFunction = DocstringFunction
        self.DocstringModule = DocstringModule
        self.parse = parse
        self.parse_auto = parse_auto
        self.parsers = parsers
        self.parse_google = parse_google
        self.parse_numpy = parse_numpy
        self.parse_sphinx = parse_sphinx
        self.infer_docstring_style = infer_docstring_style
        self.docstring_warning = docstring_warning
        self.parse_docstring_annotation = parse_docstring_annotation


class _SerializersScope(_APIScope):
    def __init__(self) -> None:
        self.JSONEncoder = JSONEncoder
        self.json_decoder = json_decoder


class _DiffScope(_APIScope):
    def __init__(self) -> None:
        self.Breakage = Breakage
        self.BreakageKind = BreakageKind
        self.find_breaking_changes = find_breaking_changes
        self.AttributeChangedTypeBreakage = AttributeChangedTypeBreakage
        self.AttributeChangedValueBreakage = AttributeChangedValueBreakage
        self.ClassRemovedBaseBreakage = ClassRemovedBaseBreakage
        self.ObjectChangedKindBreakage = ObjectChangedKindBreakage
        self.ObjectRemovedBreakage = ObjectRemovedBreakage
        self.ParameterAddedRequiredBreakage = ParameterAddedRequiredBreakage
        self.ParameterChangedDefaultBreakage = ParameterChangedDefaultBreakage
        self.ParameterChangedKindBreakage = ParameterChangedKindBreakage
        self.ParameterChangedRequiredBreakage = ParameterChangedRequiredBreakage
        self.ParameterMovedBreakage = ParameterMovedBreakage
        self.ParameterRemovedBreakage = ParameterRemovedBreakage
        self.ReturnChangedTypeBreakage = ReturnChangedTypeBreakage


class _ExtensionsScope(_APIScope):
    def __init__(self) -> None:
        self.Extensions = Extensions
        self.Extension = Extension
        self.LoadableExtensionType = LoadableExtensionType
        self.load_extensions = load_extensions
        self.builtin_extensions = builtin_extensions
        self.DataclassesExtension = DataclassesExtension


class _ExceptionsScope(_APIScope):
    def __init__(self) -> None:
        self.ExtensionError = ExtensionError
        self.ExtensionNotLoadedError = ExtensionNotLoadedError
        self.LoadingError = LoadingError
        self.UnimportableModuleError = UnimportableModuleError
        self.UnhandledEditableModuleError = UnhandledEditableModuleError
        self.NameResolutionError = NameResolutionError
        self.AliasResolutionError = AliasResolutionError
        self.CyclicAliasError = CyclicAliasError
        self.GitError = GitError
        self.GriffeError = GriffeError
        self.LastNodeError = LastNodeError
        self.RootNodeError = RootNodeError


class _GitScope(_APIScope):
    def __init__(self) -> None:
        self.assert_git_repo = assert_git_repo
        self.get_latest_tag = get_latest_tag
        self.get_repo_root = get_repo_root
        self.tmp_worktree = tmp_worktree


class _ExpressionsScope(_APIScope):
    def __init__(self) -> None:
        self.Expr = Expr
        self.ExprAttribute = ExprAttribute
        self.ExprBinOp = ExprBinOp
        self.ExprBoolOp = ExprBoolOp
        self.ExprCall = ExprCall
        self.ExprCompare = ExprCompare
        self.ExprComprehension = ExprComprehension
        self.ExprConstant = ExprConstant
        self.ExprDict = ExprDict
        self.ExprDictComp = ExprDictComp
        self.ExprExtSlice = ExprExtSlice
        self.ExprFormatted = ExprFormatted
        self.ExprGeneratorExp = ExprGeneratorExp
        self.ExprIfExp = ExprIfExp
        self.ExprJoinedStr = ExprJoinedStr
        self.ExprKeyword = ExprKeyword
        self.ExprLambda = ExprLambda
        self.ExprList = ExprList
        self.ExprListComp = ExprListComp
        self.ExprName = ExprName
        self.ExprNamedExpr = ExprNamedExpr
        self.ExprParameter = ExprParameter
        self.ExprSet = ExprSet
        self.ExprSetComp = ExprSetComp
        self.ExprSlice = ExprSlice
        self.ExprSubscript = ExprSubscript
        self.ExprTuple = ExprTuple
        self.ExprUnaryOp = ExprUnaryOp
        self.ExprVarKeyword = ExprVarKeyword
        self.ExprVarPositional = ExprVarPositional
        self.ExprYield = ExprYield
        self.ExprYieldFrom = ExprYieldFrom
        self.get_annotation = get_annotation
        self.get_base_class = get_base_class
        self.get_condition = get_condition
        self.get_expression = get_expression
        self.safe_get_annotation = safe_get_annotation
        self.safe_get_base_class = safe_get_base_class
        self.safe_get_condition = safe_get_condition
        self.safe_get_expression = safe_get_expression


class _LoggersScope(_APIScope):
    def __init__(self) -> None:
        self.Logger = Logger
        self.get_logger = get_logger
        self.logger = logger
        self.patch_loggers = patch_loggers


class _HelpersScope(_APIScope):
    def __init__(self) -> None:
        self.htree = htree
        self.vtree = vtree
        self.module_vtree = module_vtree
        self.temporary_pyfile = temporary_pyfile
        self.temporary_pypackage = temporary_pypackage
        self.temporary_visited_module = temporary_visited_module
        self.temporary_visited_package = temporary_visited_package
        self.temporary_inspected_module = temporary_inspected_module
        self.temporary_inspected_package = temporary_inspected_package
        self.TmpPackage = TmpPackage


cli = _CLIScope()
loaders = _LoadersScope()
finder = _FinderScope()
models = _ModelsScope()
agents = _AgentsScope()
docstrings = _DocstringsScope()
serializers = _SerializersScope()
diff = _DiffScope()
extensions = _ExtensionsScope()
exceptions = _ExceptionsScope()
git = _GitScope()
expressions = _ExpressionsScope()
loggers = _LoggersScope()
helpers = _HelpersScope()


__all__ = [
    "Alias",  # models, aliases
    "AliasResolutionError",  # exceptions, aliases
    "Attribute",  # models, attributes
    "AttributeChangedTypeBreakage",  # diff, attributes
    "AttributeChangedValueBreakage",  # diff, attributes
    "Breakage",  # diff
    "BreakageKind",  # diff, enums
    "BuiltinModuleError",  # exceptions, loaders
    "Class",  # models, classes
    "ClassRemovedBaseBreakage",  # diff, classes
    "CyclicAliasError",  # exceptions, aliases
    "DEFAULT_LOG_LEVEL",  # cli, logging
    "DataclassesExtension",  # extensions
    "Decorator",  # models
    "DelMembersMixin",  # models
    "Docstring",  # models, docstrings
    "DocstringAdmonition",  # docstrings
    "DocstringAttribute",  # docstrings, attributes
    "DocstringClass",  # docstrings, classes
    "DocstringDeprecated",  # docstrings
    "DocstringDetectionMethod",  # docstrings
    "DocstringElement",  # docstrings
    "DocstringFunction",  # docstrings, functions
    "DocstringModule",  # docstrings, modules
    "DocstringNamedElement",  # docstrings
    "DocstringParameter",  # docstrings, parameters
    "DocstringRaise",  # docstrings
    "DocstringReceive",  # docstrings
    "DocstringReturn",  # docstrings
    "DocstringSection",  # docstrings
    "DocstringSectionAdmonition",  # docstrings
    "DocstringSectionAttributes",  # docstrings, attributes
    "DocstringSectionClasses",  # docstrings, classes
    "DocstringSectionDeprecated",  # docstrings
    "DocstringSectionExamples",  # docstrings
    "DocstringSectionFunctions",  # docstrings, functions
    "DocstringSectionKind",  # docstrings, enums
    "DocstringSectionModules",  # docstrings, modules
    "DocstringSectionOtherParameters",  # docstrings, parameters
    "DocstringSectionParameters",  # docstrings, parameters
    "DocstringSectionRaises",  # docstrings
    "DocstringSectionReceives",  # docstrings
    "DocstringSectionReturns",  # docstrings
    "DocstringSectionText",  # docstrings
    "DocstringSectionWarns",  # docstrings, warnings
    "DocstringSectionYields",  # docstrings
    "DocstringStyle",  # docstrings
    "DocstringWarn",  # docstrings, warnings
    "DocstringYield",  # docstrings
    "ExplanationStyle",  # diff, enums
    "ExportedName",  # agents, static, exports
    "Expr",  # expressions
    "ExprAttribute",  # expressions
    "ExprBinOp",  # expressions
    "ExprBoolOp",  # expressions
    "ExprCall",  # expressions
    "ExprCompare",  # expressions
    "ExprComprehension",  # expressions
    "ExprConstant",  # expressions
    "ExprDict",  # expressions
    "ExprDictComp",  # expressions
    "ExprExtSlice",  # expressions
    "ExprFormatted",  # expressions
    "ExprGeneratorExp",  # expressions
    "ExprIfExp",  # expressions
    "ExprJoinedStr",  # expressions
    "ExprKeyword",  # expressions
    "ExprLambda",  # expressions
    "ExprList",  # expressions
    "ExprListComp",  # expressions
    "ExprName",  # expressions
    "ExprNamedExpr",  # expressions
    "ExprParameter",  # expressions
    "ExprSet",  # expressions
    "ExprSetComp",  # expressions
    "ExprSlice",  # expressions
    "ExprSubscript",  # expressions
    "ExprTuple",  # expressions
    "ExprUnaryOp",  # expressions
    "ExprVarKeyword",  # expressions
    "ExprVarPositional",  # expressions
    "ExprYield",  # expressions
    "ExprYieldFrom",  # expressions
    "Extension",  # extensions
    "ExtensionError",  # extensions, exceptions
    "ExtensionNotLoadedError",  # extensions, exceptions
    "Extensions",  # extensions
    "Function",  # models, functions
    "GetMembersMixin",  # models
    "GitError",  # git, exceptions
    "GriffeError",  # exceptions
    "GriffeLoader",  # loaders
    "Inspector",  # agents, dynamic
    "JSONEncoder",  # serializers
    "Kind",  # models, enums
    "LastNodeError",  # exceptions, ast
    "LinesCollection",  # loaders
    "LoadableExtensionType",  # extensions
    "LoadingError",  # exceptions, loaders
    "Logger",  # logging
    "LogLevel",  # logging, enums
    "Module",  # models, modules
    "ModuleFinder",  # finder, modules
    "ModulesCollection",  # loaders
    "NamePartsAndPathType",  # finder, types
    "NamePartsType",  # finder, types
    "NameResolutionError",  # exceptions, loaders
    "NamespacePackage",  # finder
    "Object",  # models
    "ObjectAliasMixin",  # models
    "ObjectChangedKindBreakage",  # diff
    "ObjectKind",  # models, enums
    "ObjectNode",  # agents, dynamic
    "ObjectRemovedBreakage",  # diff
    "Package",  # finder
    "Parameter",  # models, parameters
    "ParameterAddedRequiredBreakage",  # diff, parameters
    "ParameterChangedDefaultBreakage",  # diff, parameters
    "ParameterChangedKindBreakage",  # diff, parameters
    "ParameterChangedRequiredBreakage",  # diff, parameters
    "ParameterKind",  # enums, parameters
    "ParameterMovedBreakage",  # diff, parameters
    "ParameterRemovedBreakage",  # diff, parameters
    "Parameters",  # models, parameters
    "ParametersType",  # parameters, types
    "Parser",  # docstrings, enums
    "ReturnChangedTypeBreakage",  # diff
    "RootNodeError",  # ast, exceptions
    "SerializationMixin",  # serializers
    "SetMembersMixin",  # models
    "Stats",  # loaders
    "TmpPackage",  # helpers
    "UnhandledEditableModuleError",  # finder, exceptions
    "UnimportableModuleError",  # finder, exceptions
    "Visitor",  # agents, static
    "assert_git_repo",  # git
    "ast_children",  # ast, static
    "ast_first_child",  # ast, static
    "ast_kind",  # ast, static
    "ast_last_child",  # ast, static
    "ast_next",  # ast, static
    "ast_next_siblings",  # ast, static
    "ast_previous",  # ast, static
    "ast_previous_siblings",  # ast, static
    "ast_siblings",  # ast, static
    "builtin_decorators",  # static
    "builtin_extensions",  # static
    "c3linear_merge",  # classes
    "check",  # cli, diff
    "dump",  # cli, serializers
    "docstring_warning",  # docstrings, warnings
    "dynamic_import",  # dynamic
    "find_breaking_changes",  # diff
    "get__all__",  # expressions
    "get_annotation",
    "get_base_class",
    "get_condition",
    "get_docstring",
    "get_expression",
    "get_instance_names",
    "get_latest_tag",
    "get_logger",
    "get_name",
    "get_names",
    "get_parameters",
    "get_parser",
    "get_repo_root",
    "get_value",
    "htree",
    "infer_docstring_style",
    "inspect",
    "json_decoder",
    "load",
    "load_extensions",
    "load_git",
    "load_pypi",
    "logger",
    "main",
    "merge_stubs",
    "module_vtree",
    "parse",
    "parse_auto",
    "parse_docstring_annotation",
    "parse_google",
    "parse_numpy",
    "parse_sphinx",
    "parsers",
    "patch_loggers",
    "relative_to_absolute",
    "safe_get__all__",
    "safe_get_annotation",
    "safe_get_base_class",
    "safe_get_condition",
    "safe_get_expression",
    "safe_get_value",
    "stdlib_decorators",
    "sys_path",
    "temporary_inspected_module",
    "temporary_inspected_package",
    "temporary_pyfile",
    "temporary_pypackage",
    "temporary_visited_module",
    "temporary_visited_package",
    "tmp_worktree",
    "typing_overload",
    "visit",
    "vtree",
]