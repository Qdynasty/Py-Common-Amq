#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
from pydp_amq.apps import AMQSection

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s -  %(pathname)s - %(filename)s:%(lineno)d - %(message)s')

logger = logging.getLogger(__name__)


class BSS:
    def __init__(self):
        self.amq = AMQSection(config_dir="/Users/apple/Desktop/Trunk-Pro/common-module/pydp_amq/configs", maxsize=None)
        self.amq.signal_agent.state_agent.connect(self.act_state_callback)
        self.amq.signal_agent.order_agent.connect(self.act_orders_callback)
        self.amq.signal_agent.art_status_agent.connect(self.art_status_agent_callback)
        self.amq.signal_agent.art_orders_agent.connect(self.art_orders_agent_callback)

    def act_orders_callback(self, **kwargs):
        data = kwargs.get("data")
        logger.warning(f"source:{data.get('sender')}")
        print(kwargs)

    def act_state_callback(self, **kwargs):
        data = kwargs.get("data")
        logger.warning(f"source:{data.get('sender')}")
        print(kwargs)

    def art_status_agent_callback(self, **kwargs):
        data = kwargs.get("data")
        logger.warning(f"source:{data.get('sender')}")
        logger.warning(f"source:{data.get('sender')}")
        print(kwargs)

    def art_orders_agent_callback(self, **kwargs):
        data = kwargs.get("data")
        logger.warning(f"source:{data.get('sender')}")
        print(kwargs)


if __name__ == '__main__':

    bss = BSS()
    bss.amq.listening(["kafka"])
    # todo rmq 消息发送
    # rmq_client = bss.amq.get_client("rmq_1")
    # rmq_client.link()
    # rmq_client.publish_msg(
    #     data="hello",
    #     routing_key="fmp.v1.k.state.ActStatus.fms.A001",
    #     exchange="fmp.v1.e.topic.state",
    #     queue=""
    # )
    #
    # # todo mqtt 消息发送
    # mqtt_client = bss.amq.get_client("mqtt_1")
    # mqtt_client.link()
    # mqtt_client.publish_msg(
    #     topic="fmp/state/ArtStatus/A001",
    #     qos=1,
    #     payload="Hi"
    # )
    # print(bss.amq.callback_queue.get)
    # todo kafka
    kafka_client = bss.amq.get_client("kafka")
    kafka_client.link()
    while True:
        pass
