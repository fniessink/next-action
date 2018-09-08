#!/bin/bash
# Following this directive would mean we divert a lot from many tab completion examples:
# shellcheck disable=SC2207

_next_action()
{
  local arguments
  local argument_type="all"
  local cur=${COMP_WORDS[COMP_CWORD]}
  local prev=${COMP_WORDS[COMP_CWORD-1]}

  case ${prev} in
    --file|-f|--config-file|-c)
      COMPREPLY=( $(compgen -A "file" -- "${cur}") )
      return 0
      ;;
    --priority|-p|--reference|-r|--style|-s|--time-travel|-t)
      argument_type=${prev}
      ;;
    *)
      case ${cur} in
        @*|+*)
          argument_type=${cur:0:1}
          ;;
        -@*|-+*)
          argument_type=${cur:0:2}
          ;;
        *)
          ;;
      esac
      ;;
  esac
  arguments=$(${COMP_LINE% *} --list-arguments "${argument_type//-/_}" 2> /dev/null)
  COMPREPLY=( $(compgen -W "${arguments}" -- "${cur}") )
  return 0
}
shopt -u hostcomplete  # Needed to prevent @ from being escaped by the readline library
complete -o filenames -F _next_action next-action
