# This file is part of gwe.
#
# Copyright (c) 2018 Roberto Leinardi
#
# gwe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gwe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gwe.  If not, see <http://www.gnu.org/licenses/>.
import time
import logging
from typing import Dict, Tuple, Any

from gi.repository import Gtk, GLib, Dazzle, Gdk, GObject
from gi.repository.GObject import TYPE_DOUBLE
from injector import singleton, inject

from gwe.conf import GRAPH_COLOR_HEX
from gwe.di import HistoricalDataBuilder
from gwe.presenter.historical_data_presenter import HistoricalDataViewInterface, HistoricalDataPresenter, MONITORING_INTERVAL, \
    GraphType
from gwe.util.view import is_dazzle_version_supported
from gwe.view.graph_stacked_renderer_view import GraphStackedRenderer

_LOG = logging.getLogger(__name__)


@singleton
class HistoricalDataView(HistoricalDataViewInterface):
    @inject
    def __init__(self,
                 presenter: HistoricalDataPresenter,
                 builder: HistoricalDataBuilder,
                 ) -> None:
        _LOG.debug('init HistoricalDataView')
        self._presenter: HistoricalDataPresenter = presenter
        self._presenter.view = self
        self._builder: Gtk.Builder = builder
        self._builder.connect_signals(self._presenter)
        self._graphs: Dict[GraphType, Dict[str, Any]] = {}
        self._init_widgets()

    def _init_widgets(self) -> None:
        self._dialog: Gtk.Dialog = self._builder.get_object('dialog')
        self._init_graphs()

    def set_transient_for(self, window: Gtk.Window) -> None:
        self._dialog.set_transient_for(window)

    # pylint: disable=attribute-defined-outside-init
    def _init_graphs(self) -> None:
        if is_dazzle_version_supported():
            self._graph_views: Dict[GraphType, Tuple[Gtk.Label, Gtk.Label, Gtk.Label]] = {}
            self._graph_models: Dict[GraphType, Dazzle.GraphModel] = {}
            for graph_type in GraphType:
                self._graph_container: Gtk.Frame = self._builder.get_object(f'graph_container_{graph_type.value}')
                self._graph_views[graph_type] = (self._builder.get_object(f'graph_min_value_{graph_type.value}'),
                                                 self._builder.get_object(f'graph_max_value_{graph_type.value}'),
                                                 self._builder.get_object(f'graph_max_axis_{graph_type.value}'))
                graph_views = Dazzle.GraphView()
                graph_model = Dazzle.GraphModel()
                graph_renderer = GraphStackedRenderer()
                graph_views.set_hexpand(True)
                graph_views.props.height_request = 80
                graph_renderer.set_line_width(1.5)
                stroke_color = Gdk.RGBA()
                stroke_color.parse(GRAPH_COLOR_HEX)
                stacked_color = Gdk.RGBA()
                stacked_color.parse(GRAPH_COLOR_HEX)
                stacked_color.alpha = 0.5
                graph_renderer.set_stroke_color_rgba(stroke_color)
                graph_renderer.set_stacked_color_rgba(stacked_color)
                graph_model.set_timespan(MONITORING_INTERVAL * 1000 * 1000)
                graph_model.set_max_samples(MONITORING_INTERVAL / self._presenter.get_refresh_interval() + 1)
                graph_model.props.value_max = 100.0
                graph_model.props.value_min = 0.0

                column_ram = Dazzle.GraphColumn().new("Col0", TYPE_DOUBLE)
                graph_model.add_column(column_ram)

                graph_views.set_model(graph_model)
                graph_views.add_renderer(graph_renderer)

                self._graph_container.add(graph_views)

                graph_model_iter = graph_model.push(GLib.get_monotonic_time())
                graph_model.iter_set(graph_model_iter, 0, 0.0)

                self._graph_models[graph_type] = graph_model

    def reset_graphs(self) -> None:
        self._init_graphs()

    def refresh_graphs(self, data_dict: Dict[GraphType, Tuple[int, float, str, float, float]]) -> None:
        time1 = time.time()
        for graph_type, data_tuple in data_dict.items():
            max_value = self._graph_models[graph_type].props.value_max
            self._graph_models[graph_type].props.value_max = max(data_tuple[4], max_value)
            graph_model_iter = self._graph_models[graph_type].push(GLib.get_monotonic_time())
            self._graph_models[graph_type].iter_set(graph_model_iter, 0, data_tuple[1])
            self._graph_views[graph_type][2].set_text(f"{data_tuple[1]:.0f} {data_tuple[2]}")

            model_iter = Dazzle.GraphModelIter()
            if self._dialog.props.visible and self._graph_models[graph_type].get_iter_first(model_iter):
                min_value = data_tuple[4] * 10
                max_value = data_tuple[3]
                while Dazzle.GraphModel.iter_next(iter=model_iter):
                    gval = GObject.Value()
                    Dazzle.GraphModel.iter_get_value(iter=model_iter, column=0, value=gval)
                    val = gval.get_double()
                    min_value = min(val, min_value)
                    max_value = max(val, max_value)
                self._graph_views[graph_type][0].set_text(f"{min_value:.0f}")
                self._graph_views[graph_type][1].set_text(f"{max_value:.0f}")
                self._graph_models[graph_type].props.value_max = max(data_tuple[4], max_value)
        time2 = time.time()
        _LOG.debug(f'Refresh graph took {((time2 - time1) * 1000.0):.3f} ms')

    def show(self) -> None:
        self._dialog.show_all()

    def hide(self) -> None:
        self._dialog.hide()
