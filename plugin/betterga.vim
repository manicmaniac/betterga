if exists('g:loaded_betterga')
    finish
endif
let g:loaded_betterga = 1

let s:save_cpo = &cpo
set cpo&vim

" if b:betterga_template exists, it is prior to the global one
let g:betterga_template = '<{ci.char}> [{ci.name}] {ci.ord}, Hex {ci.hex}, Octal {ci.oct}'

command! -bar BetterAscii call betterga#ascii()
nnoremap <silent> ga :call betterga#ascii()<CR>

let &cpo = s:save_cpo
unlet s:save_cpo

