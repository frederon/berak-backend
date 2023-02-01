import React, { useState } from 'react';
import { Button, Input, Upload, message, Space, InputNumber, Tooltip } from 'antd';
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

export default function AffinePage() {
  const [plaintext, setPlaintext] = useState<string>("")
  const [keyM, setKeyM] = useState<number>(3)
  const [keyB, setKeyB] = useState<number>(1)
  const [ciphertext, setCiphertext] = useState<string>("")

  const [actionLoading, setActionLoading] = useState<boolean>(false)

  const handleEncrypt = async () => {
    setActionLoading(true)
    if (plaintext && keyM && keyB) {
      try {
        const res = await axios.post(`${BASE_API_URL}/affine/encrypt`, {
          plaintext,
          m: keyM,
          b: keyB
        })
        if (res.data.ciphertext) {
          setCiphertext(res.data.ciphertext)
        }
      } catch (err: any) {
        message.error(err.response.data.detail || "An error occured when encrypting the data")
      }
    } else {
      message.warning("Plaintext, m, and b are required")
    }
    setActionLoading(false)
  }

  const handleDecrypt = async () => {
    setActionLoading(true)
    if (ciphertext && keyM && keyB) {
      try {
        const res = await axios.post(`${BASE_API_URL}/affine/decrypt`, {
          ciphertext,
          m: keyM,
          b: keyB
        })
        if (res.data.plaintext) {
          setPlaintext(res.data.plaintext)
        }
      } catch (err: any) {
        message.error(err.response.data.detail || "An error occured when decrypting the data")
      }
    } else {
      message.warning("Ciphertext, m, and b are required")
    }
    
    setActionLoading(false)
  }

  return (
    <main>
      <h1>Affine Cipher</h1>
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
          <Tooltip title="Mx + B">
            <h2>Keys</h2>
          </Tooltip>
        </div>
        <div className="affine-keys">
          <h3>M</h3>
          <InputNumber
            value={keyM}
            onChange={
              (num) => setKeyM(num || 0)
            }
          />
          <h3>B</h3>
          <InputNumber
            value={keyB}
            onChange={
              (num) => setKeyB(num || 0)
            }
          />
        </div>
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