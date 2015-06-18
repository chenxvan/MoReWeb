import AbstractClasses
import ROOT

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = "CMSPixel_ModuleTestGroup_HighRateTest_DColEfficiencyModule_ModuleSigma_TestResult"
        self.NameSingle = "ModuleSigma"
        self.Title = "Efficiency Sigma"
        self.verbose = True
        if self.verbose:
            tag = self.Name + ": Custom Init"
            print "".ljust(len(tag), '=')
            print tag
        self.Attributes['TestedObjectType'] = 'ModuleSigma'

    def PopulateResultData(self):
        if self.verbose:
            tag = self.Name + ": Populate"
            print "".ljust(len(tag), '=')
            print tag

        dcol_eff = self.ParentObject
        chips = dcol_eff.ResultData['SubTestResults']['Chips']
        nRocs = len(chips.ResultData['SubTestResults'])

        median_list = []
        for roc in range(nRocs):
            chip = chips.ResultData['SubTestResults']['Chip' + str(roc)]

            # Get the test result from the relative efficiency
            eff = chip.ResultData['SubTestResults']['HighRateDColEfficiency'].ResultData['Plot']['ROOTObject']

            for dcol in range(26):
                median_list.append(eff.GetBinContent(dcol + 1))

        median_list.sort()
        median = median_list[len(median_list) / 2]

        # Create output histogram
        hist = ROOT.TH1F(self.GetUniqueID(), "", 20, -10, 10)

        for roc in range(nRocs):
            chip = chips.ResultData['SubTestResults']['Chip' + str(roc)]

            # Get the test result from the relative efficiency
            eff = chip.ResultData['SubTestResults']['HighRateDColEfficiency'].ResultData['Plot']['ROOTObject']

            for dcol in range(26):
                sigma = (eff.GetBinContent(dcol + 1) - median) / eff.GetBinError(dcol + 1)
                hist.Fill(sigma)

        self.ResultData['Plot']['ROOTObject'] = hist
        self.ResultData['Plot']['ROOTObject'].SetStats(False)
        self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Double Column Efficiency (Sigma)")
        self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("# DCols")
        self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
        self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
        self.ResultData['Plot']['ROOTObject'].Draw()
        self.SaveCanvas()
        
        #self.ResultData["KeyValueDictPairs"] = {
        #    "Rate" : {
        #        "Value" : 0,
        #        "Sigma" : 0,
        #        "Label" : "",
        #        "Unit" : "",
        #    },
        #}
        #
        #self.ResultData['KeyList'] = [
        #    'Rate',
        #    'Triggers',
        #    'Hits',
        #    'Insensitive pixels',
        #    'Inefficient pixels',
        #]
