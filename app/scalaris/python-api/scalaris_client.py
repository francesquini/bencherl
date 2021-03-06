#!/usr/bin/python
# Copyright 2011 Zuse Institute Berlin
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from scalaris import TransactionSingleOp, ReplicatedDHT, PubSub
from scalaris import ConnectionError, TimeoutError, NotFoundError, AbortError, KeyChangedError, UnknownError
import scalaris_bench
import sys

if __name__ == "__main__":
    if (len(sys.argv) == 3 and sys.argv[1] in ["--read", "-r"]):
        sc = TransactionSingleOp()
        key = sys.argv[2]
        try:
            value = sc.read(key)
            print 'read(' + key + ') = ' + repr(value)
        except ConnectionError as instance:
            print 'read(' + key + ') failed with connection error'
            sys.exit(1)
        except TimeoutError as instance:
            print 'read(' + key + ') failed with timeout'
            sys.exit(1)
        except NotFoundError as instance:
            print 'read(' + key + ') failed with not_found'
            sys.exit(1)
        except UnknownError as instance:
            print 'read(' + key + ') failed with unknown: ' + str(instance)
            sys.exit(1)
    elif (len(sys.argv) == 4 and sys.argv[1] in ["--write", "-w"]):
        sc = TransactionSingleOp()
        key = sys.argv[2]
        value = sys.argv[3]
        try:
            sc.write(key, value)
            print 'write(' + key + ', ' + value + '): ok'
        except ConnectionError as instance:
            print 'write(' + key + ', ' + value + ') failed with connection error'
            sys.exit(1)
        except TimeoutError as instance:
            print 'write(' + key + ', ' + value + ') failed with timeout'
            sys.exit(1)
        except AbortError as instance:
            print 'write(' + key + ', ' + value + ') failed with abort'
            sys.exit(1)
        except UnknownError as instance:
            print 'write(' + key + ', ' + value + ') failed with unknown: ' + str(instance)
            sys.exit(1)
    elif (len(sys.argv) == 5 and sys.argv[1] == "--test-and-set"):
        sc = TransactionSingleOp()
        key = sys.argv[2]
        old_value = sys.argv[3]
        new_value = sys.argv[4]
        try:
            sc.test_and_set(key, old_value, new_value)
            print 'test_and_set(' + key + ', ' + old_value + ', ' + new_value + '): ok'
        except ConnectionError as instance:
            print 'test_and_set(' + key + ', ' + old_value + ', ' + new_value + ') failed with connection error'
            sys.exit(1)
        except TimeoutError as instance:
            print 'test_and_set(' + key + ', ' + old_value + ', ' + new_value + ') failed with timeout'
            sys.exit(1)
        except AbortError as instance:
            print 'test_and_set(' + key + ', ' + old_value + ', ' + new_value + ') failed with abort'
            sys.exit(1)
        except KeyChangedError as instance:
            print 'test_and_set(' + key + ', ' + old_value + ', ' + new_value + ') failed with key_change (current old value: ' + instance.old_value + ')'
            sys.exit(1)
        except UnknownError as instance:
            print 'test_and_set(' + key + ', ' + old_value + ', ' + new_value + ') failed with unknown: ' + str(instance)
            sys.exit(1)
    elif (len(sys.argv) == 3 and sys.argv[1] in ["--delete", "-d"]):
        rdht = ReplicatedDHT()
        key = sys.argv[2]
        if len(sys.argv) >= 4:
            timeout = sys.argv[3]
        else:
            timeout = 2000
        
        try:
            ok = rdht.delete(key)
            results = rdht.get_last_delete_result()
            print 'delete(' + key + ', ' + str(timeout) + '): ok, deleted: ' + str(ok) + ' (' + repr(results) + ')'
        except TimeoutError as instance:
            results = rdht.get_last_delete_result()
            print 'delete(' + key + ', ' + str(timeout) + '): failed (timeout), deleted: ' + str(ok) + ' (' + repr(results) + ')'
        except UnknownError as instance:
            print 'delete(' + key + ') failed with unknown: ' + str(instance)
            sys.exit(1)
    elif (len(sys.argv) == 4 and sys.argv[1] in ["--publish", "-p"]):
        ps = PubSub()
        topic = sys.argv[2]
        content = sys.argv[3]
        try:
            ps.publish(topic, content)
            print 'publish(' + topic + ', ' + content + '): ok'
        except ConnectionError as instance:
            print 'publish(' + topic + ', ' + content + ') failed with connection error'
            sys.exit(1)
        except UnknownError as instance:
            print 'publish(' + topic + ', ' + content + ') failed with unknown: ' + str(instance)
            sys.exit(1)
    elif (len(sys.argv) == 4 and sys.argv[1] in ["--subscribe", "-s"]):
        ps = PubSub()
        topic = sys.argv[2]
        url = sys.argv[3]
        try:
            ps.subscribe(topic, url)
            print 'subscribe(' + topic + ', ' + url + '): ok'
        except ConnectionError as instance:
            print 'subscribe(' + topic + ', ' + url + ') failed with connection error'
            sys.exit(1)
        except TimeoutError as instance:
            print 'subscribe(' + topic + ', ' + url + ') failed with timeout'
            sys.exit(1)
        except AbortError as instance:
            print 'subscribe(' + topic + ', ' + url + ') failed with abort'
            sys.exit(1)
        except UnknownError as instance:
            print 'subscribe(' + topic + ', ' + url + ') failed with unknown: ' + str(instance)
            sys.exit(1)
    elif (len(sys.argv) == 4 and sys.argv[1] in ["--unsubscribe", "-u"]):
        ps = PubSub()
        topic = sys.argv[2]
        url = sys.argv[3]
        try:
            ps.unsubscribe(topic, url)
            print 'unsubscribe(' + topic + ', ' + url + '): ok'
        except ConnectionError as instance:
            print 'unsubscribe(' + topic + ', ' + url + ') failed with connection error'
            sys.exit(1)
        except TimeoutError as instance:
            print 'unsubscribe(' + topic + ', ' + url + ') failed with timeout'
            sys.exit(1)
        except NotFoundError as instance:
            print 'unsubscribe(' + topic + ', ' + url + ') failed with not found'
            sys.exit(1)
        except AbortError as instance:
            print 'unsubscribe(' + topic + ', ' + url + ') failed with abort'
            sys.exit(1)
        except UnknownError as instance:
            print 'unsubscribe(' + topic + ', ' + url + ') failed with unknown: ' + str(instance)
            sys.exit(1)
    elif (len(sys.argv) == 3 and sys.argv[1] in ["--getsubscribers", "-g"]):
        ps = PubSub()
        topic = sys.argv[2]
        try:
            value = ps.get_subscribers(topic)
            print 'get_subscribers(' + topic + ') = ' + repr(value)
        except ConnectionError as instance:
            print 'get_subscribers(' + topic + ') failed with connection error'
            sys.exit(1)
        except UnknownError as instance:
            print 'get_subscribers(' + topic + ') failed with unknown: ' + str(instance)
            sys.exit(1)
    elif (len(sys.argv) >= 2 and sys.argv[1] in ["--minibench", "-b"]):
        scalaris_bench.run_from_cmd(sys.argv[:1] + sys.argv[2:])
    else:
        print 'usage: ' + sys.argv[0] + ' [Options]'
        print ' -r,--read <key>'
        print '                            read an item'
        print ' -w,--write <key> <value>'
        print '                            write an item'
        print ' --test-and-set <key> <old_value> <new_value>'
        print '                            atomic test and set, i.e. write <key> to'
        print '                            <new_value> if the current value is <old_value>'
        print ' -d,--delete <key> [<timeout>]'
        print '                            delete an item (default timeout: 2000ms)'
        print '                            WARNING: This function can lead to inconsistent'
        print '                            data (e.g. deleted items can re-appear).'
        print '                            Also if an item is re-created, the version'
        print '                            before the delete can re-appear.'
        print ' -p,--publish <topic> <message>'
        print '                            publish a new message for the given topic'
        print ' -s,--subscribe <topic> <url>'
        print '                            subscribe to a topic'
        print ' -g,--getsubscribers <topic>'
        print '                            get subscribers of a topic'
        print ' -u,--unsubscribe <topic> <url>'
        print '                            unsubscribe from a topic'
        print ' -h,--help'
        print '                            print this message'
        print ' -b,--minibench [<ops> [<threads_per_node> [<benchmarks>]]]'
        print '                            run selected mini benchmark(s)'
        print '                            [1|...|9|all] (default: all benchmarks, 500'
        print '                            operations each, 10 threads per Scalaris node)'
        if len(sys.argv) == 1 or (len(sys.argv) >= 2 and not sys.argv[1] in ["--help", "-h"]):
            sys.exit(1)
