import { Link, Outlet } from "react-router-dom";

export default function Root() {
  return (
    <>
      <div id="sidebar">
        <h1>Cryptography Tucil 1</h1>
        <nav>
          <ul>
            <li>
              <Link to={`/vigenere`}>Vigenere Cipher</Link>
            </li>
            <li>
              <Link to={`/vigenere_auto`}>Auto-key Vigenere Cipher</Link>
            </li>
            <li>
              <Link to={`/vigenere_extended`}>Extended Vigenere Cipher</Link>
            </li>
            <li>
              <Link to={`/affine`}>Affine Cipher</Link>
            </li>
            <li>
              <Link to={`/playfair`}>Playfair Cipher</Link>
            </li>
            <li>
              <Link to={`/hill`}>Hill Cipher</Link>
            </li>
            <li>
              <Link to={`/enigma`}>Enigma Cipher</Link>
            </li>
          </ul>
        </nav>
      </div>
      <div id="detail">
        <Outlet />
      </div>
    </>
  );
}