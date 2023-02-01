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
import VigenereAuto from './pages/Vigenere_Auto';
import VigenereExtended from './pages/Vigenere_Extended';
import Hill from './pages/Hill';
import Playfair from './pages/Playfair';
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
      element: <VigenereAuto />,
    }, {
      path: "vigenere_extended",
      element: <VigenereExtended />,
    }, {
      path: "affine",
      element: <Affine />,
    }, {
      path: "playfair",
      element: <Playfair />,
    }, {
      path: "hill",
      element: <Hill />,
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
