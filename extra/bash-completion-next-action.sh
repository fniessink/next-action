_next_action()
{
  local cur prev
  COMPREPLY=()
  cur="${COMP_WORDS[COMP_CWORD]}"
  prev="${COMP_WORDS[COMP_CWORD-1]}"

  case "${prev}" in
    --file|-f|--config-file|-c)
      COMPREPLY=( $(compgen -A "file" -- ${cur}) )
      return 0
      ;;
    --priority|-p)
      local priorities="A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
      COMPREPLY=( $(compgen -W "${priorities}" -- ${cur}) )
      return 0
      ;;
    --reference|-r)
      local reference="always never multiple"
      COMPREPLY=( $(compgen -W "${reference}" -- ${cur}) )
      return 0
      ;;
    --style|-s)
      local styles="abap algol algol_nu arduino autumn borland bw colorful default emacs friendly fruity igor lovelace manni monokai murphy native paraiso-dark paraiso-light pastie perldoc rainbow_dash rrt tango trac vim vs xcode"
      COMPREPLY=( $(compgen -W "${styles}" -- ${cur}) )
      return 0
      ;;
    --time-travel|-t)
      local dates="tomorrow yesterday Monday Tuesday Wednesday Thursday Friday Saturday Sunday"
      COMPREPLY=( $(compgen -W "${dates}" -- ${cur}) )
      return 0
      ;;
    *)
      case "$cur" in
        @*)
          local command=${COMP_LINE% *}  # Remove $cur to prevent next-action error omessage on incomplete context
          local contexts=$(${command} --list-contexts 2> /dev/null)
          COMPREPLY=( $(compgen -W "${contexts}" -- ${cur}) )
          return 0
          ;;
        +*)
          local command=${COMP_LINE% *}  # Remove $cur to prevent next-action error message on incomplete project
          local projects=$(${command} --list-projects 2> /dev/null)
          COMPREPLY=( $(compgen -W "${projects}" -- ${cur}) )
          return 0
          ;;
        -@*)
          local command=${COMP_LINE% *}  # Remove $cur to prevent next-action error omessage on incomplete context
          local contexts=$(${command} --list-excluded-contexts 2> /dev/null)
          COMPREPLY=( $(compgen -W "${contexts}" -- ${cur}) )
          return 0
          ;;
        -+*)
          local command=${COMP_LINE% *}  # Remove $cur to prevent next-action error omessage on incomplete project
          local projects=$(${command} --list-excluded-projects 2> /dev/null)
          COMPREPLY=( $(compgen -W "${projects}" -- ${cur}) )
          return 0
          ;;
      esac
      ;;
  esac
  local arguments="@ + -@ -+ -a --all -b --blocked -c --config-file -d --due -f --file -h --help -n --number -o --overdue -p --priority -r --reference -s --style -t --time-travel -V --version"
  COMPREPLY=( $(compgen -W "${arguments}" -- ${cur}) )
  return 0
}
complete -o filenames -F _next_action next-action
