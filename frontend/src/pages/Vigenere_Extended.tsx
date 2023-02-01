import React, { useState } from 'react';
import { Button, Input, Upload, message, Space } from 'antd';
import { UploadOutlined, DownloadOutlined } from '@ant-design/icons';
import axios from 'axios';
import { BASE_API_URL } from '../constants';
import { loadFile, saveFile, toUppercaseAndFilterAlphabets } from '../utils';

const { TextArea } = Input;

const dummyRequest = async({ onSuccess }: any) => {   
   setTimeout(() => {
      onSuccess("ok");
   }, 0);
 }

export default function VigenereExtendedPage() {
  const [plaintext, setPlaintext] = useState<ArrayBuffer>(new ArrayBuffer(1))
  const [key, setKey] = useState<string>("")
  const [ciphertext, setCiphertext] = useState<ArrayBuffer>(new ArrayBuffer(1))

  const [actionLoading, setActionLoading] = useState<boolean>(false)

  const handleEncrypt = async () => {
    setActionLoading(true)
    if (plaintext && key) {
      try {
        const res = await axios.post(`${BASE_API_URL}/vigenere-extended/encrypt`, {
          plaintext,
          key,
        })
        if (res.data) {
          console.log("plaintext")
          console.log(plaintext)
          console.log(typeof(plaintext))
          console.log("ciphertext")
          console.log(res.data)
          console.log(typeof (res.data))
          
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
        const res = await axios.post(`${BASE_API_URL}/vigenere-extended/decrypt`, {
          ciphertext,
          key,
        })
        if (res.data) {
          console.log("plaintext")
          console.log(res.data)
          console.log("ciphertext")
          console.log(ciphertext)

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
          <h2>Plaintext</h2>
          <Space>
            <Upload
              onChange={(info) => loadFile(info, setPlaintext, message.error, true)}
              accept="*"
              customRequest={dummyRequest}
              showUploadList={true}
              multiple={false}
              maxCount={1}
            >
              <Button icon={<UploadOutlined />}>Load from file</Button>
            </Upload>
            <Button
              icon={<DownloadOutlined />}
              onClick={() => saveFile(plaintext, 'vigenere.txt')}
            >
              Save to file
            </Button>
          </Space>
        </div>
        {/* <TextArea
          rows={6}
          value={plaintext}
          onChange={
            (event) => setPlaintext(event.target.value)
          }
        /> */}
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
              onChange={(info) => loadFile(info, setCiphertext, message.error, true)}
              accept="*"
              customRequest={dummyRequest}
              showUploadList={true}
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
          </Space>
        </div>
        {/* <TextArea
          rows={6}
          value={ciphertext}
          onChange={
            (event) => setCiphertext(event.target.value)
          }
        /> */}
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