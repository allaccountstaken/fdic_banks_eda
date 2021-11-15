#!/bin/python
# ------------------------------------------------------------------------------
# Purpose: an interface for retrieving reports from the FFIEC site
# Usage: FFIEC_Client provides a wrapper class using zeep to interface with the
#   FFIEC SOAP servers
# Docs: python -c "import ffipy; help('ffipy.FFIEC_Client')"
# Author: Ryan Arredondo (ryan.c.arredondo@gmail.com)
# Date: 06/07/2017
# ------------------------------------------------------------------------------



import sys
import os
from warnings import warn
from configparser import ConfigParser
import zeep
from zeep.wsse.username import UsernameToken


class FFIEC_Client(zeep.Client):
    """ A wrapper class of zeep.Client for connecting to FFIEC's SOAP server.

    Args:
        Similar to parent class `zeep.Client`, except:
            `wsse` can be a tuple containing `username` and `password`, or
                `wsse` can be configured in `~/.ffiec` (or file pointed to by
                FFIEC_USER_CONF environment variable) in INI format under
                section `[wsse]`
            `wsdl` is not passed as an argument, b/c `wsdl` is constant.

    Attributes:
        Similar to parent class `zeep.Client`, except:
            `wsdl` is constant `str` pointing to the `wsdl` for the FFIEC SOAP
                server;
            `wsse_path` is a `str` pointing to the path of the `wsse`
                configuration;
            `store_login` is `bool` that if set to True will store the user's
                FFIEC login info for future use. The path of this file is
                `~/.ffiec` by default, or can be set in the environment
                variable FFIEC_USER_CONF.

    Methods:
        See https://cdr.ffiec.gov/Public/PWS/WebServices/RetrievalService.asmx
        for the methods which have been implemented.
    """
    wsdl = ('https://cdr.ffiec.gov/Public/PWS/WebServices/'
            'RetrievalService.asmx?WSDL')

    def __init__(self, wsse=None, transport=None, service_name=None,
                 port_name=None, plugins=None, 
                 strict=True,
                 xml_huge_tree=False, store_login=True):
        
        self.wsse_path = os.getenv('FFIEC_USER_CONF',
                                   os.path.join(os.environ['HOME'], '.ffiec'))
        self.wsse = wsse
        
        zeep.Client.__init__(self, self.wsdl, 
                             self.wsse, transport,
                             service_name, port_name, plugins, 
                             #strict,
                             xml_huge_tree)

        # Ensure that user login (i.e., the wsse variable) was good
        retry = self.__check_login()
        while retry and retry.startswith(('y', 'Y')):
            username, password = self.__get_login()
            self.wsse = UsernameToken(username, password)
            zeep.Client.__init__(self, self.wsdl.location, self.wsse,
                                 transport, service_name, port_name, plugins,
                                 #strict, 
                                 xml_huge_tree)
            retry = self.__check_login()

        if retry is None:
            # User gained access; save login info (as needed) for later use
            wsse_via_file = wsse is None and os.access(self.wsse_path, os.F_OK)
            if store_login and not wsse_via_file:
                self.__store_login()

    @property
    def wsse(self):
        """Returns the wsse property of the class"""
        return self.__wsse

    @wsse.setter
    def wsse(self, wsse):
        """Sets the wsse property of the class"""
        if isinstance(wsse, UsernameToken):
            self.__wsse = wsse
        elif isinstance(wsse, tuple) and len(wsse) == 2:
            self.__wsse = UsernameToken(wsse[0], wsse[1])
        elif wsse is None and os.access(self.wsse_path, os.R_OK):
            conf = ConfigParser()
            conf.read(self.wsse_path)
            self.__wsse = UsernameToken(conf['wsse']['username'],
                                        conf['wsse']['password'])
        else:
            username, password = self.__get_login()
            self.__wsse = UsernameToken(username, password)

    def __check_login(self):
        """Checks for user access and asks user to retry if no access / error.

        Args:
            None

        Returns:
            retry (str): user input to question if they want to try new login;
                returns None if user access is good.
        """
        # Try to check for access
        try:
            if self.test_user_access():  # User has access
                return None
            else:
                print('FFIEC login does not have user access...')

        # Catch any login errors and print message from error
        except zeep.exceptions.Fault as err:
            print('Error with FFIEC login: %s...\n' % err.message)

        # Give user the chance to retry
        retry = input('Would you like to try a new login? (y/n): ')
        print()

        # Warn user who does not want to retry
        if retry.startswith(('n', 'N')):
            warn('Was unable to successfully log into the FFIEC site.'
                 ' You may not be able to use class methods. To create'
                 ' an account, visit https://cdr.ffiec.gov/cdr/Public/'
                 'LegalNoticeandPrivacyPolicy.aspx in your browser.')

        return retry

    @staticmethod
    def __get_login():
        """Gets and returns user's FFIEC Login Info (username, password)."""
        username = input('Username for your FFIEC account: ')
        password = input('Password token for you FFIEC account: ')
        return username, password

    def __store_login(self):
        """Stores login info (username, password) in a conf file."""
        conf = ConfigParser()
        conf['wsse'] = {'username': self.wsse.username,
                        'password': self.wsse.password}
        with open(self.wsse_path, 'w') as f:
            conf.write(f)

    def retrieve_facsimile(self, ds_name='Call',
                           reporting_pd_end='3/31/2017',
                           fiID_type='ID_RSSD', fiID=64150,
                           facsimile_fmt='PDF',
                           outfile=None, return_result=True):
        """Retrieves a facsimile (e.g., a report) from FFIEC site.

        Args:
            ds_name (str): DataSeriesName (default is 'Call')
            reporting_pd_end (str): Date for end of the reporting period
                (default is 3/31/17)
            fiID_type (str): Type of Financial Inst ID (default is 'ID_RSSD')
            fiID (int): Financial Inst ID (default is 64150, for testing)
            facsimile_fmt (str): Format of facsimile to retrieve (default is
                'PDF')
            outfile (str): path to write facsimile to; no ouput, if None
                (default is None)
            return_result (bool): If True, return the retrieved facsimile
                (default is True)

        Returns:
            facsimile (bytes): the revtrieved facsimile (only if
                return_result==True)

        """
        # Set up kw args
        data_series = self.get_type('ns0:ReportingDataSeriesName')
        ds_name = data_series(ds_name)
        fiID_type_type = self.get_type('ns0:FinancialInstitutionIDType')
        fiID_type = fiID_type_type(fiID_type)
        facsimile_fmt_type = self.get_type('ns0:FacsimileFormat')
        facsimile_fmt = facsimile_fmt_type(facsimile_fmt)

        # Get results
        facsimile = self.service.RetrieveFacsimile(ds_name,
                                                   reporting_pd_end,
                                                   fiID_type, fiID,
                                                   facsimile_fmt)
        # Write file
        if outfile:
            mode = 'wb' if facsimile_fmt == 'PDF' else 'w'
            with open(outfile, mode) as f:
                f.write(facsimile)

        # Return results
        if return_result:
            return facsimile

    def retrieve_filers_since_date(self, ds_name='Call',
                                   reporting_pd_end='3/31/2017',
                                   last_update_date='3/31/2017'):
        """Retrieves ID RSSDs of filers after given date for given reporting pd.

        Args:
            ds_name (str): DataSeriesName (default is 'Call')
            reporting_pd_end (str): Date for end of the reporting period
                (default is 3/31/17)
            last_update_date (str): Specifies date that filers filed after
                (default is 3/31/17)

        Returns:
            filers (list of ints): ID RSSDs of filers

        """
        # Set up kw args
        data_series = self.get_type('ns0:ReportingDataSeriesName')
        ds_name = data_series(ds_name)

        # Get and return results
        filers = self.service.RetrieveFilersSinceDate(ds_name,
                                                      reporting_pd_end,
                                                      last_update_date)
        return filers

    def retrieve_filers_submission_datetime(self, ds_name='Call',
                                            reporting_pd_end='3/31/2017',
                                            last_update_date='3/31/2017'):
        """Retrieves ID RSSD, DateTime of filers after given date, reporting pd.

        Args:
            ds_name (str): DataSeriesName (default is 'Call')
            reporting_pd_end (str): Date for end of the reporting period
                (default is 3/31/17)
            last_update_date (str): Specifies date that filers filed after
                (default is 3/31/17)

        Returns:
            results (list of dicts): dict for each filer with keys 'ID_RSSD',
                'DateTime'

        """
        # Set up kw args
        data_series = self.get_type('ns0:ReportingDataSeriesName')
        ds_name = data_series(ds_name)

        # Get and return results
        results = (self.service
                   .RetrieveFilersSubmissionDateTime(ds_name,
                                                     reporting_pd_end,
                                                     last_update_date))
        return results

    def retrieve_panel_of_reporters(self, ds_name='Call',
                                    reporting_pd_end='3/31/2017'):
        """Retrieves Fin Insts in Panel of Reporters for given reporting pd.

        Args:
            ds_name (str): DataSeriesName (default is 'Call')
            reporting_pd_end (str): Date for end of the reporting period
                (default is 3/31/17)

        Returns:
            results (list of dicts): dict for each Institution with keys
                'ID_RSSD', 'FDICCertNumber', 'OCCCChartNumber',
                'OTSDockNumber', 'PrimaryABARoutNumber', 'Name', 'State',
                'City', 'Address', 'ZIP', 'FilingType',
                'HasFiledForReportingPeriod'

        """
        # Set up kw args
        data_series = self.get_type('ns0:ReportingDataSeriesName')
        ds_name = data_series(ds_name)

        # Get and return results
        results = self.service.RetrievePanelOfReporters(ds_name,
                                                        reporting_pd_end)
        return results

    def retrieve_reporting_periods(self, ds_name='Call'):
        """Retrieves end dates of financial reporting periods.

        Args:
            ds_name (str): DataSeriesName (default is 'Call')

        Returns:
            dates (list of strs): End dates of financial reporting periods

        """
        # Set up kw args
        data_series = self.get_type('ns0:ReportingDataSeriesName')
        ds_name = data_series(ds_name)

        # Get and return dates
        dates = self.service.RetrieveReportingPeriods(ds_name)
        return dates

    def retrieve_ubpr_reporting_periods(self):
        """Retrieves end dates of UBPR reporting periods.

        Args:
            None

        Returns:
            dates (list of strs): End dates of UBPR reporting periods

        """
        # Get and return dates
        dates = self.service.RetrieveUBPRReportingPeriods()
        return dates

    def retrieve_ubpr_xbrl_facsimile(self, reporting_pd_end='3/31/2017',
                                     fiID_type='ID_RSSD', fiID=64150,
                                     outfile=None, return_result=True):
        """Retrieves a UBPR facsimile in XBRL format from FFIEC site.

        Args:
            reporting_pd_end (str): Date for end of the reporting period
                (default is 3/31/17)
            fiID_type (str): Type of Financial Inst ID (default is 'ID_RSSD')
            fiID (int): Financial Inst ID (default is 64150, for testing)
            outfile (str): path to write facsimile to; no ouput, if None
                (default is None)
            return_result (bool): If True, return the retrieved facsimile
                (default is True)

        Returns:
            facsimile (bytes): the revtrieved facsimile (only if
                return_result==True)

    """
        # Set up kw args
        fiID_type_type = self.get_type('ns0:FinancialInstitutionIDType')
        fiID_type = fiID_type_type(fiID_type)

        # Get results
        facsimile = self.service.RetrieveUBPRXBRLFacsimile(reporting_pd_end,
                                                           fiID_type, fiID)

        # Write file
        if outfile:
            with open(outfile, 'w') as f:
                f.write(facsimile)

        # Return results
        if return_result:
            return facsimile

    def test_user_access(self):
        """Tests whether or not user has access to FFIEC SOAP service

        Args:
            None

        Returns:
            result (bool): True if user has access, otherwise False

        """
        result = self.service.TestUserAccess()
        return result
