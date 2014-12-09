if exists('g:loaded_betterga')
	finish
endif
let g:loaded_betterga = 1

let s:save_cpo = &cpo
set cpo&vim

nnoremap <silent> ga :call betterga#ascii()<CR>

let &cpo = s:save_cpo
unlet s:save_cpo

