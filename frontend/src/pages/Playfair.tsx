import React, { useEffect, useState } from 'react';
import { Button, Input, Upload, message, Space, Drawer } from 'antd';
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
 
const ALPHABETS = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'

export default function PlayfairPage() {
  const [plaintext, setPlaintext] = useState<string>("")
  const [key, setKey] = useState<string[][]>([])
  
  const [ciphertext, setCiphertext] = useState<string>("")

  const [actionLoading, setActionLoading] = useState<boolean>(false)
  const [drawerOpen, setDrawerOpen] = useState<boolean>(false)

  const [sentence, setSentence] = useState<string>("")

  useEffect(() => {
    let newMatrix = new Array(5)
    for (let i = 0; i < 5; i++) {
      newMatrix[i] = new Array(5)
      for (let j = 0; j < 5; j++) {
        newMatrix[i][j] = ALPHABETS[(i * 5) + j]
      }
    }
    setKey(newMatrix)
  }, [])

  const handleGenerateKey = async () => {
    setActionLoading(true)
    if (sentence) {
      try {
        const res = await axios.post(`${BASE_API_URL}/playfair/generate-key`, {
          sentence,
        })
        if (res.data.key) {
          setKey(res.data.key)
        }
      } catch (err: any) {
        message.error(err.response.data.detail || "An error occured when encrypting the data")
      }
    } else {
      message.warning("Sentence is required")
    }
    setDrawerOpen(false)
    setActionLoading(false)
  }

  const handleEncrypt = async () => {
    setActionLoading(true)
    if (plaintext && key) {
      try {
        const res = await axios.post(`${BASE_API_URL}/playfair/encrypt`, {
          plaintext,
          key,
        })
        if (res.data.ciphertext) {
          setCiphertext(res.data.ciphertext)
        }
      } catch (err: any) {
        message.error(err.response.data.detail || "An error occured when encrypting the data")
      }
    } else {
      message.warning("Plaintext and key are required")
    }
    setActionLoading(false)
  }

  const handleDecrypt = async () => {
    setActionLoading(true)
    if (ciphertext && key) {
      try {
        const res = await axios.post(`${BASE_API_URL}/playfair/decrypt`, {
          ciphertext,
          key,
        })
        if (res.data.plaintext) {
          setPlaintext(res.data.plaintext)
        }
      } catch (err: any) {
        message.error(err.response.data.detail || "An error occured when decrypting the data")
      }
    } else {
      message.warning("Ciphertext and key are required")
    }
    
    setActionLoading(false)
  }

  return (
    <main>
      <h1>Playfair Cipher</h1>
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
            <Button
              onClick={() =>
                setDrawerOpen(true)
              }
            >
              Generate key from sentence
            </Button>
          </Space>
        </div>
        <MatrixInput
          rows={5}
          columns={5}
          matrix={key}
          setMatrix={setKey}
          numbersOnly={false}
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
      <Drawer
        title="Generate Key"
        placement="right"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      >
        <Space direction='vertical'>
          <Input
            value={sentence}
            onChange={
              (event) => setSentence(event.target.value)
            }
            width="100%"
          />
          <Button
            type="primary"
            onClick={handleGenerateKey}
            loading={actionLoading}
          >
              Generate key
          </Button>
        </Space>
      </Drawer>
    </main>
  )
}