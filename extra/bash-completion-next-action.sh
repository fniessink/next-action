#!/bin/bash

_next_action()
{
  local argument_type="all"
  local cur=${COMP_WORDS[COMP_CWORD]}
  local prev=${COMP_WORDS[COMP_CWORD-1]}

  case ${prev} in
    --file|-f|--config-file|-c)
      COMPREPLY=( $(compgen -A "file" -- ${cur}) )
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
  local arguments=$(${COMP_LINE% *} --list-arguments ${argument_type//-/_} 2> /dev/null)
  COMPREPLY=( $(compgen -W "${arguments}" -- "${cur}") )
  return 0
}
COMP_WORDBREAKS=${COMP_WORDBREAKS/@/}  # Needed to prevent @ from being escaped
complete -o filenames -F _next_action next-action
