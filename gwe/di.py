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

import logging

from gi.repository import Gtk
from injector import Module, provider, singleton, Injector, Key
from peewee import SqliteDatabase
from rx.disposables import CompositeDisposable
from rx.subjects import Subject

from gwe.conf import APP_PACKAGE_NAME, APP_MAIN_UI_NAME, APP_DB_NAME, APP_EDIT_SPEED_PROFILE_UI_NAME, \
    APP_PREFERENCES_UI_NAME
from gwe.util.path import get_data_path, get_config_path

LOG = logging.getLogger(__name__)

SpeedProfileChangedSubject = Key("SpeedProfileChangedSubject")
SpeedStepChangedSubject = Key("SpeedStepChangedSubject")
MainBuilder = Key(APP_MAIN_UI_NAME)
EditSpeedProfileBuilder = Key(APP_EDIT_SPEED_PROFILE_UI_NAME)
PreferencesBuilder = Key(APP_PREFERENCES_UI_NAME)


# pylint: disable=no-self-use
class ProviderModule(Module):
    @singleton
    @provider
    def provide_main_builder(self) -> MainBuilder:
        LOG.debug("provide Gtk.Builder")
        builder = Gtk.Builder()
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_file(get_data_path(APP_MAIN_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_edit_speed_profile_builder(self) -> EditSpeedProfileBuilder:
        LOG.debug("provide Gtk.Builder")
        builder = Gtk.Builder()
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_file(get_data_path(APP_EDIT_SPEED_PROFILE_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_preferences_builder(self) -> PreferencesBuilder:
        LOG.debug("provide Gtk.Builder")
        builder = Gtk.Builder()
        builder.set_translation_domain(APP_PACKAGE_NAME)
        builder.add_from_file(get_data_path(APP_PREFERENCES_UI_NAME))
        return builder

    @singleton
    @provider
    def provide_thread_pool_scheduler(self) -> CompositeDisposable:
        LOG.debug("provide CompositeDisposable")
        return CompositeDisposable()

    @singleton
    @provider
    def provide_database(self) -> SqliteDatabase:
        LOG.debug("provide CompositeDisposable")
        return SqliteDatabase(get_config_path(APP_DB_NAME))

    @singleton
    @provider
    def provide_speed_profile_changed_subject(self) -> SpeedProfileChangedSubject:
        return Subject()

    @singleton
    @provider
    def provide_speed_step_changed_subject(self) -> SpeedStepChangedSubject:
        return Subject()


INJECTOR = Injector(ProviderModule)
