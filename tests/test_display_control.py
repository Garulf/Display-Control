import asyncio

import display_control
from display_control import BRIGHTNESS_STEPS, context_menu, query, set_luminance


def titles(results):
    return [result.title for result in results]


def test_lists_each_monitor_with_its_brightness_then_all_monitors(displays):
    results = query("")
    assert titles(results) == ["Monitor 1", "Monitor 2", "All Monitors"]
    assert [result.subtitle for result in results[:2]] == ["Brightness: 80", "Brightness: 30"]
    assert [result.context_data for result in results] == [[0], [1], [None]]
    assert all(result.icon == "icon.png" for result in results)


def test_query_filters_by_title_case_insensitively(displays):
    assert titles(query("MONITOR 2")) == ["Monitor 2"]
    assert titles(query("tv")) == []


def test_all_monitors_is_hidden_with_a_single_monitor(displays):
    displays.pop()
    assert titles(query("")) == ["Monitor 1"]


def test_context_menu_offers_brightness_steps(displays):
    results = context_menu([1])
    assert titles(results) == ["100%", "75%", "50%", "25%", "0%"]
    assert results[2].subtitle == "Set brightness to 50%"
    assert results[2].icon == "brightness.png"
    action = results[2].to_json()["JsonRPCAction"]
    assert action["Method"] == "set_luminance"
    assert action["Parameters"] == [50, 1]


def test_context_menu_for_all_monitors_passes_no_index(displays):
    actions = [result.to_json()["JsonRPCAction"] for result in context_menu([None])]
    assert [action["Parameters"] for action in actions] == [[step, None] for step in BRIGHTNESS_STEPS]


def test_context_menu_without_context_data_is_empty():
    assert context_menu(None) == []
    assert context_menu([]) == []


def test_set_luminance_on_one_monitor(displays):
    set_luminance(25, 1)
    assert displays[0].calls == []
    assert displays[1].calls == [("set_luminance", 25)]


def test_set_luminance_on_all_monitors(displays):
    set_luminance(100, None)
    assert [monitor.luminance for monitor in displays] == [100, 100]


def test_plugin_registers_flow_launcher_methods():
    events = display_control.plugin._event_handler._events
    assert {"query", "context_menu", "set_luminance"} <= set(events)


def test_query_through_the_jsonrpc_dispatcher(displays):
    response = asyncio.run(display_control.plugin._event_handler.trigger_event("query", "monitor 1"))
    assert [item["Title"] for item in response["Result"]] == ["Monitor 1"]
