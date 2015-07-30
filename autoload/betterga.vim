if has('python3')
    let s:python = 'python3'
    let s:pyfile = 'py3file'
elseif has('python')
    let s:python = 'python'
    let s:pyfile = 'pyfile'
else
    echoerr 'betterga requires python interface.'
    finish
endif

let s:save_cpo = &cpo
set cpo&vim

let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

execute s:pyfile s:plugin_path.'/betterga.py'

function! s:current_char()
    return matchstr(getline('.'), '.', col('.') - 1)
endfunction

function! betterga#describe(char)
    execute s:python 'BetterGA.betterga(vim.eval("a:char"))'
endfunction

function! betterga#ascii()
    call betterga#describe(s:current_char())
endfunction

let &cpo = s:save_cpo
unlet s:save_cpo

