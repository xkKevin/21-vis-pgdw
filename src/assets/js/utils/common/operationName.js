export function drawOperationName(g,pos,name,dy='1.2em',colFontSize) {
    let showText = ''
    if(30 >= name.length){
        showText = name
    }else{
        showText = name.slice(0,29)
        showText += '…'
    }
    g.append("text")
        .text(name)
        .attr("x", pos[0])
        .attr("y", pos[1])
        .attr('text-anchor','middle')
        .attr('dy',dy)
        .attr('font-size',`${colFontSize * 2}px`)
        .text(showText)
        .append("svg:title")
        .text(name)
}