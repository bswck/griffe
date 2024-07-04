"""Griffe package.

Signatures for entire Python programs.
Extract the structure, the frame, the skeleton of your project,
to generate API documentation or find breaking changes in your API.
"""

from __future__ import annotations

from slothy import lazy_importing

with lazy_importing():
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
    from _griffe.dataclasses import (
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
    from _griffe.docstrings.dataclasses import (
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
    from _griffe.docstrings.google import parse_google
    from _griffe.docstrings.numpy import parse_numpy
    from _griffe.docstrings.parsers import parse, parsers
    from _griffe.docstrings.sphinx import parse_sphinx
    from _griffe.docstrings.utils import DocstringWarningCallable, docstring_warning, parse_docstring_annotation
    from _griffe.encoders import JSONEncoder, json_decoder
    from _griffe.enumerations import (
        BreakageKind,
        DocstringSectionKind,
        ExplanationStyle,
        Kind,
        ObjectKind,
        ParameterKind,
        Parser,
        When,
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
        ExtensionType,
        InspectorExtension,
        LoadableExtensionType,
        VisitorExtension,
        builtin_extensions,
        load_extensions,
    )
    from _griffe.extensions.dataclasses import DataclassesExtension
    from _griffe.extensions.hybrid import HybridExtension
    from _griffe.finder import ModuleFinder, NamePartsAndPathType, NamePartsType, NamespacePackage, Package
    from _griffe.git import assert_git_repo, get_latest_tag, get_repo_root, tmp_worktree
    from _griffe.importer import dynamic_import, sys_path
    from _griffe.loader import GriffeLoader, load, load_git
    from _griffe.logger import LogLevel, get_logger, patch_loggers
    from _griffe.merger import merge_stubs
    from _griffe.mixins import (
        DelMembersMixin,
        GetMembersMixin,
        ObjectAliasMixin,
        SerializationMixin,
        SetMembersMixin,
    )
    from _griffe.stats import Stats
    from _griffe.tests import (
        TmpPackage,
        htree,
        module_vtree,
        temporary_inspected_module,
        temporary_pyfile,
        temporary_pypackage,
        temporary_visited_module,
        temporary_visited_package,
        vtree,
    )

# Regenerate this list with the following Python snippet:
# import griffe
# names = sorted(n for n in dir(griffe) if not n.startswith("_") and n not in ("annotations", "lazy_importing"))
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
    "ExtensionType",
    "Extensions",
    "Function",
    "GetMembersMixin",
    "GitError",
    "GriffeError",
    "GriffeLoader",
    "HybridExtension",
    "Inspector",
    "InspectorExtension",
    "JSONEncoder",
    "Kind",
    "LastNodeError",
    "LinesCollection",
    "LoadableExtensionType",
    "LoadingError",
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
    "VisitorExtension",
    "DocstringWarningCallable",
    "When",
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
    "inspect",
    "json_decoder",
    "load",
    "load_extensions",
    "load_git",
    "main",
    "merge_stubs",
    "module_vtree",
    "parse",
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
    "temporary_pyfile",
    "temporary_pypackage",
    "temporary_visited_module",
    "temporary_visited_package",
    "tmp_worktree",
    "typing_overload",
    "visit",
    "vtree",
    "docstring_warning",
]
