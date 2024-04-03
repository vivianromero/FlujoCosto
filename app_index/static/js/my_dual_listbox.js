$(function () {
    let dfilterTextClear = window.data.filterTextClear
    let dfilterPlaceHolder = window.data.filterPlaceHolder
    let dmoveSelectedLabel = window.data.moveSelectedLabel
    let dmoveAllLabel = window.data.moveAllLabel
    let dremoveSelectedLabel = window.data.removeSelectedLabel
    let dremoveAllLabel = window.data.removeAllLabel
    let dinfoText1 = window.data.infoText1
    let dinfoText2 = window.data.infoText2
    let dinfoTextFiltered = window.data.infoTextFiltered
    let dinfoTextEmpty = window.data.infoTextEmpty
    $('.duallistbox').bootstrapDualListbox({
        filterTextClear: dfilterTextClear,
        filterPlaceHolder: dfilterPlaceHolder,
        moveSelectedLabel: dmoveSelectedLabel,
        moveAllLabel: dmoveAllLabel,
        removeSelectedLabel: dremoveSelectedLabel,
        removeAllLabel: dremoveAllLabel,
        infoText1: dinfoText1,
        infoText2: dinfoText2,
        infoTextFiltered: dinfoTextFiltered,
        infoTextEmpty: dinfoTextEmpty,
        selectorMinimalHeight: 125,
    })
})