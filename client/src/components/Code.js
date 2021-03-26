import React, {useContext, useState, useRef, useEffect} from 'react';
import codeContext from '../context/Code/CodeContext';
import {Button, Layout, Row, Col, Typography, Modal, Table, Form, Input, Spin, message, Tabs} from "antd";

import Emulator from "./Emulator";
import Editor from "./Editor";

const {Header, Footer, Content} = Layout;
const {Title} = Typography;
const FormItem = Form.Item;
const TabPane = Tabs.TabPane

const Code = () => {
  return (
    <>
      <CodeIn/>
      <ModalCodesMain/>
      <ModalFormMain/>
    </>
  )
}

const ModalCodesMain = () => {
  const [modalCodesShow, setModalCodesShow] = useState(false);

  const ModalCodes = () => {
    const CodeContext = useContext(codeContext);
    const [filter, setFilter] = useState("examples")

    useEffect(() => {
      CodeContext.getCodes(filter)
    }, [filter])

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

    const ModalTable = () => {
      return (
        <Table columns={columns} dataSource={CodeContext.codes} rowKey='pk'/>
      )
    }

    return (
      <>
        <Tabs
          defaultActiveKey="examples"
          centered
          onChange={(key) => {
            setFilter(key)
            CodeContext.getCodes(filter)
          }}
        >
          <TabPane
            tab={
              <span style={{width: 200}}>
                Examples
               </span>
            }
            key="examples">
          </TabPane>
          <TabPane
            tab={
              <span style={{width: 200}}>
                Approved
               </span>
            }
            key="approved">
          </TabPane>
          <TabPane
            tab={
              <span>
                All
               </span>
            }
            key="all">
          </TabPane>
        </Tabs>
        <ModalTable/>
      </>
    )
  }

  return (
    <>
      <Button onClick={() => {
        setModalCodesShow(true)
      }}>Codes</Button>

      <Modal
        title="Codes"
        style={{}}
        width={1000}
        visible={modalCodesShow}
        onOk={() => setModalCodesShow(false)}
        onCancel={() => setModalCodesShow(false)}
        footer={[]}
      >
        <ModalCodes/>
      </Modal>

    </>
  )
}

const ModalFormMain = () => {
  const [modalFormShow, setModalFormShow] = useState(false);

  const ModalForm = () => {
    const form = useRef(null);
    const [sending, setSending] = useState(false)
    const CodeContext = useContext(codeContext);

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
                  message.success('Successfully sent animation');
                })
                .catch(() => {
                  message.error('Sending animation failed');
                  setSending(false)
                })
            }}
          >
            <FormItem
              label="Name"
              name="name"
              rules={[{required: true, message: 'Please input a name!'}]}
            >
              <Input/>
            </FormItem>
            <FormItem
              label="Author"
              name="author"
              rules={[{required: true, message: 'Please input a author name!'}]}
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
      <Button onClick={() => {
        setModalFormShow(true)
      }}>Submit</Button>
      <ModalForm/>
    </>
  )
}

const CodeIn = () => {
  const CodeContext = useContext(codeContext);

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
      </Layout>
    </>
  )

};

export default Code;