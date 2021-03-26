import React, {useContext, useState, useRef} from 'react';
import codeContext from '../context/Code/CodeContext';
import {Button, Layout, Row, Col, Typography, Modal, Table, Form, Input, Spin} from "antd";

import Emulator from "./Emulator";
import Editor from "./Editor";

const {Header, Footer, Content} = Layout;
const {Title} = Typography;
const FormItem = Form.Item;

const Code = () => {
  const CodeContext = useContext(codeContext);
  const [modalCodesShow, setModalCodesShow] = useState(false);
  const [modalFormShow, setModalFormShow] = useState(false);

  const columns = [{
    title: 'Name',
    dataIndex: 'name',
    render: (text, record) => (
      <span>
      <a onClick={() => {
        setModalCodesShow(false)
        CodeContext.setCode(record.code)
      }}>{record.name}</a>
    </span>
    ),
  }, {
    title: 'Author',
    dataIndex: 'author',
  }, {
    title: 'Description',
    dataIndex: 'description',
  }]

  const ModalCodes = () => {
    return (
      <Modal
        title="Codes"
        style={{}}
        width={1000}
        visible={modalCodesShow}
        onOk={() => setModalCodesShow(false)}
        onCancel={() => setModalCodesShow(false)}
        footer={[]}
      >
        <Table columns={columns} dataSource={CodeContext.codes} rowKey='pk'/>
      </Modal>
    )
  }

  const ModalForm = () => {
    const form = useRef(null);
    const [sending, setSending] = useState(false)

    return (
      <Modal
        title="Submit"
        style={{}}
        width={1000}
        visible={modalFormShow}
        onOk={(f) => {
          form.current.submit()
        }}
        onCancel={() => setModalFormShow(false)}
      >
        <Spin spinning={sending}>
        <Form
          name="normal_login"
          ref={form}
          onFinish={(e) => {
            console.log(e)
            setSending(true)
            CodeContext.submitCode(e)
              .then(() => {
                setSending(false)
                setModalFormShow(false)
              })
          }}
        >
          <FormItem
            label="Name"
            name="name"
          >
            <Input/>
          </FormItem>
          <FormItem
            label="Author"
            name="author"
          >
            <Input/>
          </FormItem>
          <FormItem
            label="Description"
            name="description"
          >
            <Input/>
          </FormItem>
        </Form>
        </Spin>
      </Modal>
    )
  }

  return (
    <>
      <Layout>
        <Header style={{'backgroundColor': '#fff'}}>
          <Row>
            <Col>
              <Title>Emulator</Title>
            </Col>
            <Col>
              <Button onClick={() => {
                CodeContext.setCode(CodeContext.code + '!')
              }}>Run</Button>
            </Col>
          </Row>
        </Header>
        <Content>
          <Row>
            <Col xs={24} xl={12}>
              <Emulator/>
            </Col>
            <Col xs={24} xl={12}>
              <Editor/>
            </Col>
          </Row>
        </Content>
        <Footer>
          <Button onClick={() => {
            CodeContext.getCodes()
              .then(() => {
                setModalCodesShow(true)
              })
          }}>Codes</Button>
          <Button onClick={() => {
            setModalFormShow(true)
          }}>Submit</Button>
        </Footer>
      </Layout>
      <ModalCodes/>
      <ModalForm/>
    </>
  )

};

export default Code;