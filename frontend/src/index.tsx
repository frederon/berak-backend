import React from 'react';
import ReactDOM from 'react-dom/client';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Root from './pages/Root'
import ErrorPage from './pages/Error';
import Affine from './pages/Affine';
import Vigenere from './pages/Vigenere';
import 'antd/dist/reset.css';
import './index.scss';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [{
      path: "vigenere",
      element: <Vigenere />,
    }, {
      path: "vigenere_auto",
      element: <h1>Vigenere Auto</h1>,
    }, {
      path: "vigenere_extended",
      element: <h1>Vigenere Extended</h1>,
    }, {
      path: "affine",
      element: <Affine />,
    }, {
      path: "playfair",
      element: <h1>Playfair</h1>,
    }, {
      path: "hill",
      element: <h1>Hill</h1>,
    }, {
      path: "enigma",
      element: <h1>Enigma</h1>,
    }]
  },
]);

root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
