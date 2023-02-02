import { InputNumber, Select, Space } from 'antd';
import React from 'react';

const EnigmaInput = ({
  index,
  rotors,
  setRotors,
  positions,
  setPositions,
  rings,
  setRings
}: {
  index: number,
  rotors: number[],
  positions: number[],
  rings: number[]
  setRotors: React.Dispatch<React.SetStateAction<number[]>>,
  setPositions: React.Dispatch<React.SetStateAction<number[]>>,
  setRings: React.Dispatch<React.SetStateAction<number[]>>,
}) => {

  const handleRotorsChange = (value: number) => {
    const result = [...rotors];
    result[index] = value;
    setRotors(result)
  }

  const handlePositionsChange = (value: number | null) => {
    if (value) {
      const result = [...positions];
      result[index] = value-1;
      setPositions(result)
    }
  }

  const handleRingsChange = (value: number | null) => {
    if (value) {
      const result = [...rings];
      result[index] = value-1;
      setRings(result)
    }
  }

  const intToChar = (num: number) => {
    return String.fromCharCode(num + 64)
  }
  

  return (
    <Space>
      <Space direction='vertical'>
        <span>Rotor { index + 1}</span>
        <Select
          value={rotors[index]}
          style={{ width: 120 }}
          onChange={handleRotorsChange}
          options={[
            { value: 0, label: 'I' },
            { value: 1, label: 'II' },
            { value: 2, label: 'III' },
            { value: 3, label: 'IV' },
          ]}
        />
      </Space>
      <Space direction='vertical'>
        <span>Position</span>
        <InputNumber
          style={{ width: 120 }}
          addonAfter={intToChar(positions[index]+1)}
          value={positions[index]+1}
          min={1}
          max={26}
          onChange={handlePositionsChange}
        />
      </Space>
      <Space direction='vertical'>
        <span>Ring</span>
        <InputNumber
          style={{ width: 120 }}
          addonAfter={intToChar(rings[index]+1)}
          value={rings[index]+1}
          min={1}
          max={26}
          onChange={handleRingsChange}
        />
      </Space>
    </Space>
  );
};

export default EnigmaInput;