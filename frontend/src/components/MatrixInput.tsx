import React from 'react';

const MatrixInput = ({
  rows,
  columns,
  matrix,
  setMatrix,
  numbersOnly,
}: {
  rows: number,
  columns: number,
  matrix: any[][],
  setMatrix: React.Dispatch<React.SetStateAction<any>>,
  numbersOnly: boolean
}) => {
  const handleChange = (event: any, rowIndex: number, colIndex: number) => {
    const updatedMatrix = [...matrix];
    if (numbersOnly) {
      updatedMatrix[rowIndex][colIndex] = Number(event.target.value);
    } else {
      updatedMatrix[rowIndex][colIndex] = event.target.value;
    }
    setMatrix(updatedMatrix);
  };

  return (
    <table>
      <tbody>
        {matrix.map((row, rowIndex) => (
          <tr key={rowIndex}>
            {row.map((col, colIndex) => (
              <td key={colIndex}>
                <input
                  type={numbersOnly ? "number" : "text"}
                  value={col}
                  onChange={(e) => handleChange(e, rowIndex, colIndex)}
                />
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default MatrixInput;
