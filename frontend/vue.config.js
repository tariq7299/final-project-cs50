const { defineConfig } = require('@vue/cli-service');
const Dotenv = require('dotenv-webpack');

module.exports = defineConfig({
  transpileDependencies: true,

  configureWebpack: {
    plugins: [
      new Dotenv()
    ]
  },

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  },
  pwa: {
    manifestOptions: {
      name: 'GoldGardyn',
      short_name: 'GoldGardyn',
    }
  }
  // devServer: {
  //   host: '0.0.0.0',
  //   port: 8083
  // }

});
