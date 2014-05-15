# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from sure import scenario

from pyeqs import QuerySet, Filter
from pyeqs.dsl import Terms
from tests.helpers import prepare_data, cleanup_data, add_document


@scenario(prepare_data, cleanup_data)
def test_simple_search(context):
    """
    Perform simple match_all search
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz"})

    # And I do a search
    results = t[0:1]

    # Then I get a the expected results
    len(results).should.equal(1)
    results[0]['_source'].should.equal({"bar": "baz"})


@scenario(prepare_data, cleanup_data)
def test_terms_search(context):
    """
    Perform simple terms filter
    """
    # When create a queryset
    t = QuerySet("localhost", index="foo")

    # And there are records
    add_document("foo", {"bar": "baz", "foo": "foo"})
    add_document("foo", {"bar": "bazbaz", "foo": "foo"})
    add_document("foo", {"bar": "baz", "foo": "foofoo"})
    add_document("foo", {"bar": "baz", "foo": "foofoofoo"})

    # And I filter for terms
    t.filter(Terms("foo", ["foo", "foofoo"]))
    results = t[0:10]

    # Then I get a the expected results
    len(results).should.equal(3)
