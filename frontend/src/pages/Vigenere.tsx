import React, { useState } from 'react';
import { Button, Input, Upload, message, Space } from 'antd';
import { UploadOutlined, DownloadOutlined } from '@ant-design/icons';
import axios from 'axios';
import { BASE_API_URL } from '../constants';
import { loadFile, saveFile, spacesEvery5Chars, toUppercaseAndFilterAlphabets } from '../utils';

const { TextArea } = Input;

const dummyRequest = async({ onSuccess }: any) => {   
   setTimeout(() => {
      onSuccess("ok");
   }, 0);
 }

export default function VigenerePage() {
  const [plaintext, setPlaintext] = useState<string>("")
  const [key, setKey] = useState<string>("")
  const [ciphertext, setCiphertext] = useState<string>("")

  const [actionLoading, setActionLoading] = useState<boolean>(false)

  const handleEncrypt = async () => {
    setActionLoading(true)
    if (plaintext && key) {
      const res = await axios.post(`${BASE_API_URL}/vigenere/encrypt`, {
        plaintext,
        key,
      })
      setCiphertext(res.data.ciphertext)
    } else {
      message.warning("Plaintext and key are required")
    }
    setActionLoading(false)
  }

  const handleDecrypt = async () => {
    setActionLoading(true)
    if (ciphertext && key) {
      const res = await axios.post(`${BASE_API_URL}/vigenere/decrypt`, {
        ciphertext,
        key,
      })
      setPlaintext(res.data.plaintext)
    } else {
      message.warning("Ciphertext and key are required")
    }
    
    setActionLoading(false)
  }

  return (
    <main>
      <h1>Vigenere Cipher</h1>
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
        </div>
        <Input
          value={key}
          onChange={
            (event) => setKey(
              toUppercaseAndFilterAlphabets(
                event.target.value
              )
            )
          }
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
    </main>
  )
}