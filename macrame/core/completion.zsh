# Macrame tab-completion script to be sourced with the Z shell.
# Known to work on zsh 5.0.x, probably works on later 4.x releases as well (as
# it uses the older compctl completion system).

_complete_macrame() {
    # `words` contains the entire command string up til now (including
    # program name).
    #
    # We hand it to macrame so it can figure out the completion.
    #
    # `reply` is the array of valid completions handed back to `compctl`.
    reply=( $(python -m macrame --complete "${words}" ) )
}


# Tell shell builtin to use the above for completing our given binary name(s).
# * -K: use given function name to generate completions.
# * +: specifies 'alternative' completion, where options after the '+' are only
#   used if the completion from the options before the '+' result in no matches.
# * -f: when function generates no results, use filenames.
# * positional args: program names to complete for.
compctl -K _complete_macrame + -f macrame mac
