//seleciona os itens clicad

var menuItem = document.querySelectorAll('.iten-menu')

function selectLink(){
    menuItem.forEach((item)=>
        item.classList.remove('ativo')
    )
    this.classList.add('ativo')
}

menuItem.forEach((item)=>
    item.addEventListener('click', selectLink)
)

//expandir o menu

var btnExp = document.querySelector('#btnc-exp')
var menuSide = document.querySelector('.side-menu')

btnExp.addEventListener('click', function(){
    menuSide.classList.toggle('expandir')
})