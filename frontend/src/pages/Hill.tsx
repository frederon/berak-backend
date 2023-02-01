import React, { useEffect, useState } from 'react';
import { Button, Input, Upload, message, Space, InputNumber } from 'antd';
import { UploadOutlined, DownloadOutlined } from '@ant-design/icons';
import axios from 'axios';
import { BASE_API_URL } from '../constants';
import { loadFile, saveFile, spacesEvery5Chars, toUppercaseAndFilterAlphabets } from '../utils';
import MatrixInput from '../components/MatrixInput';

const { TextArea } = Input;

const dummyRequest = async({ onSuccess }: any) => {   
   setTimeout(() => {
      onSuccess("ok");
   }, 0);
 }

export default function HillPage() {
  const [plaintext, setPlaintext] = useState<string>("")
  const [keySize, setKeySize] = useState<number>(3)
  const [key, setKey] = useState<number[][]>([])
  
  const [ciphertext, setCiphertext] = useState<string>("")

  const [actionLoading, setActionLoading] = useState<boolean>(false)

  useEffect(() => {
    let newMatrix = new Array(keySize)
    for (let i = 0; i < keySize; i++) {
      newMatrix[i] = new Array(keySize).fill(0)
    }
    setKey(newMatrix)
  }, [keySize])

  const handleEncrypt = async () => {
    setActionLoading(true)
    if (plaintext && key && keySize) {
      try {
        const res = await axios.post(`${BASE_API_URL}/hill/encrypt`, {
          plaintext,
          key,
          m: keySize
        })
        if (res.data.ciphertext) {
          setCiphertext(res.data.ciphertext)
        }
      } catch (err: any) {
        message.error(err.response.data.detail || "An error occured when encrypting the data")
      }
    } else {
      message.warning("Plaintext, key, and key size are required")
    }
    setActionLoading(false)
  }

  const handleDecrypt = async () => {
    setActionLoading(true)
    if (ciphertext && key && keySize) {
      try {
        const res = await axios.post(`${BASE_API_URL}/hill/decrypt`, {
          ciphertext,
          key,
          m: keySize
        })
        if (res.data.plaintext) {
          setPlaintext(res.data.plaintext)
        }
      } catch (err: any) {
        message.error(err.response.data.detail || "An error occured when decrypting the data")
      }
    } else {
      message.warning("Ciphertext, key, and key size are required")
    }
    
    setActionLoading(false)
  }

  return (
    <main>
      <h1>Hill Cipher</h1>
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
          <h2>Key</h2>
          <Space>
            <h3>Key size</h3>
            <InputNumber
              value={keySize}
              onChange={
                (num) => setKeySize(num || 0)
              }
            />
          </Space>
        </div>
        <MatrixInput
          rows={keySize}
          columns={keySize}
          matrix={key}
          setMatrix={setKey}
          numbersOnly={true}
        />
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