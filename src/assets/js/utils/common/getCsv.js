import * as d3 from 'd3'
export function getCsv(path){
    return new Promise((resolve, reject) => {
        d3.text(path).then(data => {
            let tempData = d3.csvParseRows(data)
            resolve(tempData)
        })
        // d3.dsv(",",path).then((data) => {
        //     let keys = data[0]
        //     let table = [[]]
        //     for(let key in keys){
        //         table[0].push(key)
        //     }
        //     for(let row = 1;row < data.length;row ++){
        //         let tempRow = []
        //         for(let idx = 0;idx < table[0].length;idx++){
        //             tempRow.push(data[row][table[0][idx]])
        //         }
        //         table.push(tempRow)
        //     }
        //     resolve(table)
        // });
    })
}