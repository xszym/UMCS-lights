import React, {useContext, useState} from 'react';
import codeContext from '../context/Code/CodeContext';
import {Button, Layout, Row, Col, Typography, Modal, Table, Form, Input} from "antd";

import Emulator from "./Emulator";
import Editor from "./Editor";

const { Header, Footer, Content } = Layout;
const { Title } = Typography;
const FormItem = Form.Item;

const columns = [{
  title: 'Name',
  dataIndex: 'name',
  render: (text, record) => (
    <span>
      <a onClick={() => {
        console.log('open')
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

const Code = () => {
  const CodeContext = useContext(codeContext);
  const [modalCodesShow, setModalCodesShow] = useState(false);
  const [modalFormShow, setModalFormShow] = useState(false);

  const ModalCodes = () => {
    return (
      <Modal
        title="Codes"
        style={{ }}
        width={1000}
        visible={modalCodesShow}
        onOk={() => setModalCodesShow(false)}
        onCancel={() => setModalCodesShow(false)}
        footer={[]}
      >
        <Table columns={columns} dataSource={CodeContext.codes} rowKey='pk' />
      </Modal>
    )
  }

  const ModalForm = () => {
    return (
      <Modal
        title="Submit"
        style={{}}
        width={1000}
        visible={modalFormShow}
        onOk={() => setModalFormShow(false)}
        onCancel={() => setModalFormShow(false)}
      >
        <Form>
          <FormItem
            label="Name"
          >
            <Input />
          </FormItem>
          <FormItem
            label="Author"
          >
            <Input />
          </FormItem>
          <FormItem
            label="Description"
          >
            <Input />
          </FormItem>
        </Form>
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
          <Button onClick={() => {setModalFormShow(true)}}>Submit</Button>
        </Footer>
      </Layout>
      <ModalCodes />
      <ModalForm />
    </>
  )

};

export default Code;