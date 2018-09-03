_next_action()
{
  COMPREPLY=()
  local argument_type="all"
  local arguments=""
  local cur="${COMP_WORDS[COMP_CWORD]}"
  local prev="${COMP_WORDS[COMP_CWORD-1]}"

  case "${prev}" in
    --file|-f|--config-file|-c)
      COMPREPLY=( $(compgen -A "file" -- ${cur}) )
      return 0
      ;;
    --priority|-p)
      argument_type="priorities"
      ;;
    --reference|-r)
      argument_type="reference"
      ;;
    --style|-s)
      argument_type="styles"
      ;;
    --time-travel|-t)
      arguments="tomorrow yesterday Monday Tuesday Wednesday Thursday Friday Saturday Sunday"
      ;;
    *)
      case "$cur" in
        @*)
          argument_type="contexts"
          ;;
        +*)
          argument_type="projects"
          ;;
        -@*)
          argument_type="excluded_contexts"
          ;;
        -+*)
          argument_type="excluded_projects"
          ;;
      esac
      ;;
  esac
  if [ "$arguments" == "" ]
  then
    arguments=$(${COMP_LINE% *} --list-arguments ${argument_type} 2> /dev/null)
  fi 
  COMPREPLY=( $(compgen -W "${arguments}" -- ${cur}) )
  return 0
}
complete -o filenames -F _next_action next-action
