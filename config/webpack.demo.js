import path from 'path';
import {fileURLToPath} from 'url';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import CopyWebpackPlugin from 'copy-webpack-plugin';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default {
  mode: 'production',
  devtool: 'source-map',
  entry: {
    viewer: './app/pacs/viewer.js',
  },
  output: {
    filename: '[name].min.js',
    path: path.resolve(__dirname, '../build/demo'),
    clean: true,
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './app/pacs/index.html',
      filename: 'index.html',
      scriptLoading: 'module',
      chunks: ['viewer'],
    }),
    new CopyWebpackPlugin({
      patterns: [
        {
          from: 'app/data/SE1/original',
          to: 'data/se1/original',
          noErrorOnMissing: false,
        },
        {
          from: 'app/favicon.ico',
          to: 'favicon.ico',
          noErrorOnMissing: false,
        },
      ],
    }),
  ],
};