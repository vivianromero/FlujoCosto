let child_div_unidad_contable = $('#div_id_idunidadcontable').children()[1]
if (child_div_unidad_contable) {
    $(child_div_unidad_contable).attr(
        'style', 'height:200px; overflow-y:scroll; border-style: solid; border-width: 1px; padding-left: 5px; border-color: lightgray;'
    )
}
let child_div_departamento_destino = $('#div_id_relaciondepartamento').children()[1]
if (child_div_departamento_destino) {
    $(child_div_departamento_destino).attr(
        'style', 'height:200px; overflow-y:scroll; border-style: solid; border-width: 1px; padding-left: 5px; border-color: lightgray;'
    )
}
let child_div_departamentoproducto = $('#div_id_departamentoproducto').children()[1]
if (child_div_departamentoproducto) {
    $(child_div_departamentoproducto).attr(
        'style', 'height:200px; overflow-y:scroll; border-style: solid; border-width: 1px; padding-left: 5px; border-color: lightgray;'
    )
}
