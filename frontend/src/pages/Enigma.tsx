import React, { useState } from 'react';
import { Button, Input, Upload, message, Space, Tooltip } from 'antd';
import { UploadOutlined, DownloadOutlined } from '@ant-design/icons';
import axios from 'axios';
import { BASE_API_URL } from '../constants';
import { loadFile, saveFile, spacesEvery5Chars, toUppercaseAndFilterAlphabets } from '../utils';
import EnigmaInput from '../components/EnigmaInput';

const { TextArea } = Input;

const dummyRequest = async({ onSuccess }: any) => {   
   setTimeout(() => {
      onSuccess("ok");
   }, 0);
 }

export default function EnigmaPage() {
  const [plaintext, setPlaintext] = useState<string>("")
  const [rotors, setRotors] = useState<number[]>([0, 0, 0])
  const [positions, setPositions] = useState<number[]>([0, 0, 0])
  const [rings, setRings] = useState<number[]>([0, 0, 0])
  const [plugboard, setPlugboard] = useState<string>("")
  const [ciphertext, setCiphertext] = useState<string>("")

  const [actionLoading, setActionLoading] = useState<boolean>(false)

  const handleEncrypt = async () => {
    setActionLoading(true)
    const plugboardFormatted = constructPlugboard(plugboard.trim())
    if (plaintext && validateKeys() && plugboardFormatted) {
      try {
        const res = await axios.post(`${BASE_API_URL}/enigma/encrypt`, {
          plaintext,
          rotors,
          positions,
          rings,
          plugboard: plugboardFormatted
        })
        if (res.data.ciphertext) {
          setCiphertext(res.data.ciphertext)
        }
      } catch (err: any) {
        message.error(err.response.data.detail || "An error occured when encrypting the data")
      }
    } else {
      message.warning("Inputs are invalid")
    }
    setActionLoading(false)
  }

  const handleDecrypt = async () => {
    setActionLoading(true)
    const plugboardFormatted = constructPlugboard(plugboard.trim())
    if (ciphertext && validateKeys() && plugboardFormatted) {
      try {
        const res = await axios.post(`${BASE_API_URL}/enigma/decrypt`, {
          ciphertext,
          rotors,
          positions,
          rings,
          plugboard: plugboardFormatted
        })
        if (res.data.plaintext) {
          setPlaintext(res.data.plaintext)
        }
      } catch (err: any) {
        message.error(err.response.data.detail || "An error occured when decrypting the data")
      }
    } else {
      message.warning("Inputs are invalid")
    }
    
    setActionLoading(false)
  }

  const validateKeys = () => {
    return rotors.length === 3 && positions.length === 3 && rings.length === 3
  }

  const constructPlugboard = (plugboard: string) => {
    const plugboard_splitted = plugboard.split(' ')
    const result: any = {}
    console.log(plugboard_splitted)
    for (const data of plugboard_splitted) {
      if (data) {
        if (data.length !== 2) {
          message.error(`Invalid plugboard format: pairs of letters to be swapped expected (e.g 'ab cd ef')`)
          return false;
        }
        result[data[0].toUpperCase()] = data[1].toUpperCase()
      }
    }
    return result
  }

  return (
    <main>
      <Tooltip title="Enigma M3 UKW-B Reflector">
        <h1 style={{
          display: 'inline-block'
        }}>
          Enigma Cipher
        </h1>
      </Tooltip>
      <div className="plaintext">
        <div className="title-and-actions">
          <h2>Plaintext</h2>
          <Space>
            <Upload
              onChange={(info) => loadFile(info, setPlaintext, message.error)}
              accept="text/*"
              customRequest={dummyRequest}
              showUploadList={false}
              multiple={false}
              maxCount={1}
            >
              <Button icon={<UploadOutlined />}>Load from file</Button>
            </Upload>
            <Button
              onClick={() =>
                setPlaintext(
                  toUppercaseAndFilterAlphabets(plaintext)
                )
              }
            >
              Format plaintext
            </Button>
            <Button
              onClick={() =>
                setPlaintext(
                  spacesEvery5Chars(plaintext)
                )
              }
            >
              Group every 5 characters
            </Button>
          </Space>
        </div>
        <TextArea
          rows={6}
          value={plaintext}
          onChange={
            (event) => setPlaintext(event.target.value)
          }
        />
      </div>
      <div className="key">
        <div className="title-and-actions">
          <h2>Keys</h2>
        </div>
        <Space direction="vertical">
          {[0, 1, 2].map(val => (
            <EnigmaInput
              key={val}
              index={val}
              rotors={rotors}
              setRotors={setRotors}
              positions={positions}
              setPositions={setPositions}
              rings={rings}
              setRings={setRings}
            />
          ))}
          <span>Plugboard</span>
          <Input
            value={plugboard}
            onChange={
              (event) => setPlugboard(event.target.value)
            }
          />
        </Space>
      </div>
      <div className="ciphertext">
        <div className="title-and-actions">
          <h2>Ciphertext</h2>
          <Space>
            <Upload
              onChange={(info) => loadFile(info, setCiphertext, message.error)}
              accept="text/*"
              customRequest={dummyRequest}
              showUploadList={false}
              multiple={false}
              maxCount={1}
            >
              <Button icon={<UploadOutlined />}>Load from file</Button>
            </Upload>
            <Button
              icon={<DownloadOutlined />}
              onClick={() => saveFile(ciphertext, 'vigenere.txt')}
              disabled={ciphertext.length === 0}
            >
              Save to file
            </Button>
            <Button
              onClick={() =>
                setCiphertext(
                  toUppercaseAndFilterAlphabets(ciphertext)
                )
              }
            >
              Format ciphertext
            </Button>
            <Button
              onClick={() =>
                setCiphertext(
                  spacesEvery5Chars(ciphertext)
                )
              }
            >
              Group every 5 characters
            </Button>
          </Space>
        </div>
        <TextArea
          rows={6}
          value={ciphertext}
          onChange={
            (event) => setCiphertext(event.target.value)
          }
        />
      </div>
      <div className="actions">
        <Space>
          <Button
            type="primary"
            size="large"
            onClick={handleEncrypt}
            loading={actionLoading}
          >
              Encrypt
          </Button>
          <Button
            size="large"
            onClick={handleDecrypt}
            loading={actionLoading}
          >
              Decrypt
          </Button>
        </Space>
      </div>
    </main>
  )
}