import React, { useState } from 'react';
import { Button, Input, Upload, message, Space } from 'antd';
import { UploadOutlined, DownloadOutlined, ClearOutlined } from '@ant-design/icons';
import FormData from 'form-data';
import axios from 'axios';
import { BASE_API_URL } from '../constants';
import { loadFile, saveFile, toUppercaseAndFilterAlphabets } from '../utils';

const dummyRequest = async({ onSuccess }: any) => {   
   setTimeout(() => {
      onSuccess("ok");
   }, 0);
 }

export default function VigenereExtendedPage() {
  const [plaintext, setPlaintext] = useState<ArrayBuffer>(new ArrayBuffer(0))
  const [key, setKey] = useState<string>("")
  const [ciphertext, setCiphertext] = useState<ArrayBuffer>(new ArrayBuffer(0))

  const [actionLoading, setActionLoading] = useState<boolean>(false)

  const handleEncrypt = async () => {
    setActionLoading(true)
    if (plaintext && key) {
      try {
        const form = new FormData()
        form.append('plainfile', new Blob([plaintext]))
        form.append('key', key)

        const res = await axios.post(`${BASE_API_URL}/vigenere-extended/encrypt`, form, {
          headers: {
            'Accept': 'application/octet-stream',
            'Content-Type': 'multipart/form-data'
          },
          responseType: 'arraybuffer'
        })

        if (res.data) {          
          setCiphertext(res.data)
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
        const form = new FormData()
        form.append('cipherfile', new Blob([ciphertext]))
        form.append('key', key)

        const res = await axios.post(`${BASE_API_URL}/vigenere-extended/decrypt`, form, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          responseType: 'arraybuffer'
        })

        if (res.data) {
          setPlaintext(res.data)
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
      <h1>Extended Vigenere Cipher</h1>
      <div className="plaintext">
        <div className="title-and-actions">
          <h2>Plainfile</h2>
        </div>
        <Space direction='vertical'>
          <Upload
            onChange={(info) => loadFile(info, setPlaintext, message.error, true)}
            accept="*"
            customRequest={dummyRequest}
            showUploadList={false}
            multiple={false}
            maxCount={1}
          >
            <Button icon={<UploadOutlined />}>Load from file</Button>
          </Upload>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => saveFile(plaintext, 'vigenere_extended')}
            disabled={plaintext.byteLength === 0}
          >
            Save to file
          </Button>
          <Button
            icon={<ClearOutlined />}
            onClick={() => setPlaintext(new ArrayBuffer(0))}
            disabled={plaintext.byteLength === 0}
          >
            Clear file
          </Button>
        </Space>
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
          <h2>Cipherfile</h2>
        </div>
        <Space direction='vertical'>
          <Upload
            onChange={(info) => loadFile(info, setCiphertext, message.error, true)}
            accept="*"
            customRequest={dummyRequest}
            showUploadList={false}
            multiple={false}
            maxCount={1}
          >
            <Button icon={<UploadOutlined />}>Load from file</Button>
          </Upload>
          <Button
            icon={<DownloadOutlined />}
            onClick={() => saveFile(ciphertext, 'vigenere_extended')}
            disabled={ciphertext.byteLength === 0}
          >
            Save to file
          </Button>
          <Button
            icon={<ClearOutlined />}
            onClick={() => setCiphertext(new ArrayBuffer(0))}
            disabled={ciphertext.byteLength === 0}
          >
            Clear file
          </Button>
        </Space>
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