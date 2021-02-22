import * as d3 from 'd3'
import {drawIcon} from "../utils/icon"
import {drawOperationName} from "../utils/operationName";
import {drawTableForRow} from "../utils/createTableForRow";
import {fontSize, svgSize} from "../config/config";

export function combine_tables_inner_join(m1,m2,m3,rule,t1_name,t2_name,t3_name,inColors2,outColor,name,showTableName){
    if(!showTableName){
        t1_name = ''
        t2_name = ''
        t3_name = ''
    }
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    // svg.setAttribute('style', 'border: 1px solid black');
    svg.setAttribute('id', `mainsvg${name}`);
    svg.setAttribute('width', svgSize.width);
    svg.setAttribute('height', svgSize.height);
    svg.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
    document.getElementById('glyphs').appendChild(svg)

    let width = d3.select(`#mainsvg${name}`).attr('width') - 20
    let height = d3.select(`#mainsvg${name}`).attr('height')
    let colWidth = width / (m1[0].length + m3[0].length + 1)
    let colHeight = height / (m1.length + 8)
    let colFontSize = fontSize.colFontSize
    let cellFontSize = fontSize.cellFontSize
    const g = d3.select(`#mainsvg${name}`).append('g')
        .attr('transform',`translate(10,10)`)

    drawTableForRow(g,m1,[0, colHeight],colWidth,colHeight,t1_name,colFontSize,cellFontSize)
    drawTableForRow(g,m2,[0, 2.5 * colHeight + m1.length * colHeight],colWidth,colHeight,t2_name,colFontSize,cellFontSize,inColors2)

    let arrowUrl = require('../../images/arrow.png')
    drawIcon(g,[(m1[0].length + 0.1) * colWidth,(1 + m1.length / 2) * colHeight - colHeight / 2 + colHeight * 2],0.8 * colWidth, colHeight,arrowUrl)

    drawTableForRow(g,m3,[(m1[0].length + 1) * colWidth,4 * colHeight],colWidth,colHeight,t3_name,colFontSize,cellFontSize,outColor)

    let yOfLine = (m1.length + m2.length + 3) * colHeight
    drawOperationName(g,[width / 2,yOfLine],`${rule}`,'1.2em',colFontSize)
}
