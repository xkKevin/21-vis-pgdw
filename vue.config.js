module.exports = {
    devServer: {
        // 自动打开浏览器
        open: true,
        port: 8081,
        proxy: {
            '/': {
                target: 'http://localhost',
                ws: true,
                changeOrigin: true,
                pathRewrite: {
                    '^/': '/'
                }
            },
            // '/api': {
            //     target: 'http://localhost',
            //     ws: true,
            //     changeOrigin: true,
            //     pathRewrite: {
            //         // '^/api/(.*)': '$1/'
            //         '^/api': '/'
            //     }
            // }
        }
    },
    publicPath: './',
    outputDir: 'dist',
    assetsDir: 'static'
}