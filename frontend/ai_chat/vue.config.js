const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

// module.exports = {
//   devServer: {
//     proxy: 'http://localhost:8000'
//   }
// };

// module.exports = {
//   devServer: {
//     proxy: {
//       '/message': {
//         target: 'http://localhost:8000',
//         changeOrigin: true,
//       },
//       '/newsession': {
//         target: 'http://localhost:8000',
//         changeOrigin: true,
//       },
//       '/chat_history': {
//         target: 'http://localhost:8000',
//         changeOrigin: true,
//       },
//       // '/': {
//       //   target: 'http://localhost:8000',
//       //   changeOrigin: true,
//       // },
//     },
//   },
// };

