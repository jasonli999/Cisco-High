# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class CH_Automation(object):
    '''Creates the parent class with functions that are used in every sub-class'''
    
    def __init__(self):
        '''Defines the parent variables, self.xlsxs is the dict of all of the Excel sheets defined'''
        self.uniquesites = {}
        self.xlsxs = {}
    
    def addXLSX(self, xlsx, name):
        '''Creates a DataFrame and assigns it a name to be callable in the sub-classes; name is a str, xlsx has to be fill address in this format:''' # xlsx = r"C:\Users\jasoli3\Downloads\2022 Extern Details.xlsx"
        self.xlsxs[name] = pd.read_excel(xlsx)
        self.xlsxs[name].dropna(how = 'all', inplace = True)

    def sort(self, name, columnnum):
        '''sort() sorts a named Excel sheet by a certian column. name is a str that has to match a corresponding Excel sheet added by addXLSX(). 
        columnnum is a list that describes which columns to sort by level of importance.'''
        columnname = []
        for i in range(len(columnnum)):
            self.df.keys()[i-1]
        if type(columnnum) == list:
            self.xlsxs[name].sort_values(by=columnname, inplace = True)
        self.xlsxs[name].reset_index(drop = True, inplace = True)
        return self.xlsxs[name]

    def columnrange(self, name, column):
        '''columnrange() returns a dict of the ranges in which a uniqe value occurs in a sorted, named DataFrame. name is a str that has to match a corresponding Excel sheet added by addXLSX().
        columnnum is a int of the column that the ranges are to be retrieved from.'''
        self.uniquesites = {}
        self.sort(name, [column])
        for i in self.xlsxs[name].index:
            if i == 0:
                self.uniquesites[self.xlsxs[name].values[i][column-1]] = [i]
            else:
                if i < self.xlsxs[name].index[len(self.xlsxs[name].index)-1]:
                    if self.xlsxs[name].values[i][column-1] != self.xlsxs[name].values[i+1][column-1]:
                        self.uniquesites[self.xlsxs[name].values[i][column-1]].append(i)
                        self.uniquesites[self.xlsxs[name].values[i+1][column-1]] = [i+1]
                else:
                    self.uniquesites[self.xlsxs[name].values[i][column-1]].append(i)
        return self.uniquesites
    
    def uniquevalcount(self, name, statcolumn, rows = None):
        '''uniquevalcount() returns a dict of the number of times a unique values occurs in a column of a named DataFrame. name is a str that has to match a corresponding Excel sheet added by addXLSX().
        statcolumn is the number of the column to be analyzed, rows is an optional call to manipulate the specific rows the algorithm searches through.'''
        uniqval = {}
        columnname = self.df.keys()[statcolumn-1]
        if type(rows) == list:
            vals = ((self.xlsxs[name][columnname])[rows[0]:rows[1]+1]).dropna(how = 'all').to_numpy()
        else:
            vals = (self.xlsxs[name][columnname].dropna(how = 'all')).to_numpy()
        uniqvals = np.unique(vals)
        for i in uniqvals:
            uniqval[i] = 0
        for i in vals:
            for j in uniqval:
                if i == j:
                    uniqval[j] += 1
        return uniqval

class Extern_Details(CH_Automation):
    
    def __init__(self, xlsx):
        '''Creates an inheritance of variables and functions from CH_Automation(). xlsx is an Excel file which is to be named Extern_Details.'''
        CH_Automation.__init__(self)
        CH_Automation.addXLSX(self, xlsx, 'Extern_Details')
        self.uniquevals = {}
        self.name = 'Extern_Details'
        self.df = self.xlsxs[self.name]

class Demographics(Extern_Details):
    
    def __init__(self, xlsx):
        '''Creates an inheritance of variables and functions from Extern_Details(). xlsx is an Excel file which is to be named Extern_Details.'''
        Extern_Details.__init__(self, xlsx)
        self.demostat = {}
    
    def demostatistics(self, statcolumn, rows = None):
        '''demostatistics() returns a dict of the percentage that a unique value occurs in a certian column. statcolumn is the column number of the column that the algorithm searches, it's an int.
        rows is an optional call that can be changed to change the rows the algorithm searches through, it's a list.'''
        vals, tot = CH_Automation.uniquevalcount(self, self.name, statcolumn, rows), 0
        for i in vals:
            tot += vals[i]
        for i in vals:
            vals[i] = str(round(vals[i]/tot * 100, 2)) + ' %'
        return vals
    
    def sitestat(self, sitename, sitecolumn, statcolumn):
        '''sitestat() returns a dict of the percentage that a unique value occurs in a certian column per site. sitename is a str, sitecolumn is an int.
        sitename corresponds to the name of a site in sitecolumn which is to be targeted.
        statcolumn is the column number of the column that the algorithm searches, it's an int.
        rows is an optional call that can be changed to change the rows the algorithm searches through, it's a list.'''
        sites, siterange = CH_Automation.columnrange(self, self.name, sitecolumn), ''
        for i in sites:
            if i == sitename:
                siterange = sites[i]
        sitestat = self.demostatistics(statcolumn, siterange)
        return sitestat
    
    def piechart(self, statcolumn):
        '''piechart() generates a piechart according to the data from demostatistics(), statcolumn is a int corresponding to the column which the algorithm searches through.'''
        title, label = self.df.keys()[statcolumn-1], []
        uniqval = CH_Automation.uniquevalcount(self, self.name, statcolumn)
        for i in uniqval:
            label.append(i)
        values = []
        for i in uniqval:
            values.append(uniqval[i])
        values = np.array(values)
        plt.pie(values, labels = label)
        plt.title(title)
        plt.show()
    
    def sitepiechart(self, sitename, sitecolumn, statcolumn):
        '''sitepiechart() generates a piechart according to the data from sitestatistics(), sitename is a str, sitecolumn is an int.
        sitename corresponds to the name of a site in sitecolumn which is to be targeted.
        statcolumn is the column number of the column that the algorithm searches, it's an int.
        rows is an optional call that can be changed to change the rows the algorithm searches through, it's a list.'''
        title, label = self.df.keys()[statcolumn-1], []
        sites, siterange = CH_Automation.columnrange(self, self.name, sitecolumn), ''
        for i in sites:
            if i == sitename:
                siterange = sites[i]
        uniqval = CH_Automation.uniquevalcount(self, self.name, statcolumn, siterange)
        for i in uniqval:
            label.append(i)
        values = []
        for i in uniqval:
            values.append(uniqval[i])
        values = np.array(values)
        plt.pie(values, labels = label)
        plt.title(title)
        plt.show()

class Capstone_Groups(Extern_Details):
    
    def __init__(self, xlsx):
        Extern_Details.__init__(self, xlsx)
        self.attr = {}
        self.groups = []
        self.groupnum = 0
        self.groupsize = []
        self.groupavg = []
        self.placegroup = []
    
    def assignNum(self, attribute, val = 'Preset'):
        '''This function assigns the numerical value associate with a certian demographic attribute. attribute is a str. Outputs an int'''
        if val == 'Preset':
            if attribute == 'RTP':
                return 0
            elif attribute == 'Richardson':
                return .33
            elif attribute == 'Herndon':
                return .67
            elif attribute == 'California':
                return 1
            elif attribute == 'Atlanta':
                return 0
            elif attribute == 'Chicago':
                return .25
            elif attribute == 'NYC':
                return .5
            elif attribute == 'Toronto':
                return .75
            elif attribute == 'St. Louis':
                return 1
            elif attribute == 'Male' or attribute == 'Man':
                return 0
            elif attribute == 'Female' or attribute == 'Woman':
                return 1
            elif attribute == 'Transgender':
                return 1.5
            elif attribute in ('African American', 'Black', 'Black / African American', '/African American'):
                return 0
            elif attribute == 'Latin / Spanish' or attribute == 'Spanish / Hispanic / Latino':
                return .17
            elif attribute == 'Pacific Islander':
                return .33
            elif attribute == 'Caucasian' or attribute == 'White / Caucasian':
                return .5
            elif attribute == 'Asian':
                return .67
            elif attribute == 'Other':
                return .83
            elif attribute == 'Prefer Not to Answer':
                return 1
            elif attribute == None or pd.isna(attribute):
                return .5
            
            elif type(val) == dict:
                for i in val:
                    if attribute == i:
                        return val[i]
                    elif attribute == None or pd.isna(attribute):
                        return .5 
        
    def defAttributes(self, namecolumn, sitecolumn, gendercolumn, racecolumn, rows = None):
        '''defAttribute creates a dict with the names of the externs and the numerical value associated with them. initialrow & finalrow are ints, representing the initial and final
            rows the algorithm searches through, namecolumn, sitecolumn, gendercolumn, and racecolumn are ints, they are the columns those details are located in.'''
        dataframe = self.df.values
        if rows == None:
            for i in range(len(dataframe)):
                self.attr[dataframe[i][namecolumn-1]] = [self.assignNum(dataframe[i][sitecolumn-1]), self.assignNum(dataframe[i][gendercolumn-1]), self.assignNum(dataframe[i][racecolumn-1])]
        elif type(rows) == list:
            for i in range(rows[0], rows[1]):
                self.attr[dataframe[i][namecolumn-1]] = [self.assignNum(dataframe[i][sitecolumn-1]), self.assignNum(dataframe[i][gendercolumn-1]), self.assignNum(dataframe[i][racecolumn-1])]
        return self.attr
        
    def groupSizes(self, groupnum):
        '''groupSizes splits the total number of externs into equal groups, groupnum is an int representing the number of groups the externs are to be split into.
            Outputs a list of group sizes'''
        self.groupnum = groupnum
        num, remainder = np.floor(
            len(self.attr)/self.groupnum), (len(self.attr) % self.groupnum)
        for i in range(self.groupnum):
            self.groupsize.append(num)
        for i in range(remainder):
            self.groupsize[i] += 1
        for i in range(len(self.groupsize)):
            self.groupsize[i] = int(self.groupsize[i])
        return self.groupsize

    def assignTarget(self):
        '''assignTarget calculates the target numbers for different demographic attributes based on the demographic ratios in the sample. Outputs a list of target values.'''
        targets = []
        for i in range(len(list(self.attr.values())[0])):
            target = 0
            for j in range(len(self.attr)):
                target += list(self.attr.values())[j][i]
            target = target/int(len(self.attr))
            targets.append(target)
        return targets

    def createGroup(self, groups, iterations, groupiter):
        '''createGroup recursively creates a group based on the numerical values calculated in assignTarget. iterations and groupiter are ints, groups is a dict
            iterations is the number of iterations the function has done already and groupiter is the number of people in the created group, 
            groups is the dict of externs and demographic values. Outputs a list of capstone groups and the experimental demographic numerical values for the groups.'''
        targets = self.assignTarget()
        if iterations == 0:
            self.placegroup.append(
                [list(groups.keys())[0], list(groups.values())[0]])
            del groups[list(groups.keys())[0]]
            self.groupavg.append(
                [list(self.placegroup)[0][1][0], len(self.placegroup)])
            self.groupavg.append(
                [list(self.placegroup)[0][1][1], len(self.placegroup)])
            self.groupavg.append(
                [list(self.placegroup)[0][1][2], len(self.placegroup)])
        avgnum = {}
        for name in groups:
            avgs = [(list(groups[name])[0] + (self.groupavg[0][0]*self.groupavg[0][1]))/(self.groupavg[0][1]+1), (list(groups[name])[1] + (self.groupavg[1]
                    [0]*self.groupavg[1][1]))/(self.groupavg[1][1]+1), (list(groups[name])[2] + (self.groupavg[2][0]*self.groupavg[2][1]))/(self.groupavg[2][1]+1)]
            for j in range(len(targets)):
                avgs[j] = abs(targets[j] - avgs[j])
            placeavgnum = sum(avgs)/3
            avgnum[name] = placeavgnum
        choice = list(avgnum.keys())[0]
        for name in avgnum:
            if avgnum[name] < avgnum[choice]:
                choice = name
        self.placegroup.append([choice, groups[choice]])
        self.groupavg[0][0] = self.groupavg[0][0] * \
            self.groupavg[0][1] + groups[choice][0]
        self.groupavg[1][0] = self.groupavg[1][0] * \
            self.groupavg[1][1] + groups[choice][1]
        self.groupavg[2][0] = self.groupavg[2][0] * \
            self.groupavg[2][1] + groups[choice][2]
        self.groupavg[0][1] += 1
        self.groupavg[1][1] += 1
        self.groupavg[2][1] += 1
        self.groupavg[0][0] = self.groupavg[0][0]/self.groupavg[0][1]
        self.groupavg[1][0] = self.groupavg[1][0]/self.groupavg[1][1]
        self.groupavg[2][0] = self.groupavg[2][0]/self.groupavg[2][1]
        groups.pop(choice)
        choice = ''
        if iterations < groupiter - 2:
            self.createGroup(groups, iterations + 1, groupiter)
        if iterations <= groupiter - 2:
            del groups
            return self.placegroup, self.groupavg

    def assignGroups(self):
        '''Calls createGroup multiple times to create the appropriate number of groups for the externs. It returns a list of the groups.'''
        groupiter, self.placegroup, grouptarget = self.groupsize, [], []
        groups = self.attr.copy()
        for size in groupiter:
            self.groupavg, self.placegroup = [], []
            groupnames = []
            group, groupavg = self.createGroup(groups, 0, size)
            grouptarget.append([groupavg[0][0], groupavg[1][0], groupavg[2][0]])
            for i in range(len(group)):
                groupnames.append(group[i][0])
            self.groups.append(groupnames)
        return self.groups, grouptarget
    
    def targetError(self):
        '''targetError calculates the percent error of the groups made by assignGroups in comparison to the calculated target numbers in assingTarget
            It returns a list of the average percent errors of each group.'''
        target = self.assignTarget()
        groups, grouptarget = self.assignGroups()
        error = []
        for i in range(len(grouptarget)):
            error1 = abs(grouptarget[i][0] - target[0])/ target[0]
            error2 = abs(grouptarget[i][1] - target[1])/ target[1]
            error3 = abs(grouptarget[i][2] - target[2])/ target[2]
            error.append(str(round(((error1 + error2 + error3)/3)*100, 2)) + ' %')
        return error

class CH_Swag(Extern_Details):
    
    def __init__(self, xlsx):
        Extern_Details.__init__(self, xlsx)
        self.name = 'Extern_Details'
        self.df = self.xlsxs[self.name]
        self.createdf = {'Name':[], 'Type':[], 'Size':[], 'Email':[], 'Address': [], 'City':[], 'State':[], 'Country':[]}
    
    def classifyAddress(self, address):
        statelist = {'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN',
        'Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV',
        'New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC',
        'South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY','Alberta':'AB','British Columbia':'BC','Manitoba':'MB',
        'New Brunswick':'NB','Newfoundland and Labrador':'NL','Nova Scotia':'NS','Ontario':'ON','Prince Edward Island':'PE','Quebec':'QC','Saskatchewan':'SK'}
        state, city, zipcode, country = '', '', '',''
        actualaddress = ''
        address = address.split(' ')
        for i in range(len(address)):
            address[i] = address[i].replace(',', '')
            address[i] = address[i].replace('.', '')
        for name in statelist:
            for j in range(len(address)):
                if name.lower() == address[j].lower() or statelist[name].lower() == address[j].lower():
                    state = name
                    statenum = j
        if state != '':
            city = address[statenum-1]
            for i in range(statenum, len(address)):
                if address[i].lower() in ['us', 'usa']:
                    country = 'United States'
                if address[i].lower() == 'united' and address[i+1].lower() == 'states':
                    country = 'United States'
                if address[i].lower() in ['canada', 'ca']:
                    country = 'Canada'
                try:
                    if len(str(int(address[i]))) == 5:
                        zipcode = str(address[i])
                except:
                    None
                letternum, intnum = 0,0
                if len(address[i]) == 6:
                    letters = [*address[i]]
                    for item in letters:
                        try:
                            if type(int(item)) == int:
                                intnum += 1
                        except:
                            letternum += 1
                    if letternum == 3 and intnum == 3:
                        zipcode = address[i]
                if len(address[i]) == 3 and len(address[i+1]) == 3:
                    letters = [*(address[i]+address[i+1])]
                    for item in letters:
                        try:
                            if type(int(item)) == int:
                                intnum += 1
                        except:
                            letternum += 1
                    if letternum == 3 and intnum == 3:
                        zipcode = address[i] + address[i+1]
            address = address[0:statenum-1]
            for item in address:
                actualaddress += item + ' '
        else:
            for item in address:
                actualaddress += item + ' '
            city, state, zipcode, country = None, None, None, None
                
        return actualaddress, city, state, zipcode, country
    
    def addDemographics(self, namecolumn, sizecolumn, emailcolumn, addresscolumn):
        namecolumnname, sizecolumnname, emailcolumnname, addresscolumnname = self.df.keys()[namecolumn-1], self.df.keys()[sizecolumn-1], self.df.keys()[emailcolumn-1], self.df.keys()[addresscolumn-1]
        self.createdf['Name'] = self.df[namecolumnname].to_numpy()
        self.createdf['Size'] = self.df[sizecolumnname].to_numpy()
        self.createdf['Email'] = self.df[emailcolumnname].to_numpy()
        
        return self.createdf
    
class Daily_Survey(CH_Automation):

    def __init__(self, xlsx):
        CH_Automation.__init__(self)
        CH_Automation.addXLSX(self, xlsx, 'Daily_Survey')
        self.uniquevals = {}
        self.sessionrating = {}
        self.name = 'Daily_Survey'
        self.df = self.xlsxs[self.name]
        
    def sessionratings(self, sessioncolumn, ratingcolumn, rows = None, sort = False):
        if type(rows) == list and sort == True:
            sessionname, ratingname = self.df.keys()[sessioncolumn-1], self.df.keys()[ratingcolumn-1]
            sessionval, ratingval = self.df[sessionname].to_numpy()[rows[0]:rows[1]+1], self.df[ratingname].to_numpy()[rows[0]:rows[1]+1]
            sessionnum = CH_Automation.uniquevalcount(self, self.name, sessioncolumn, rows)
            uniqsessions = {}
            uniq = np.unique(((self.df[sessionname])[rows[0]:rows[1]+1]).dropna(how = 'all').to_numpy())
        else:
            sessionname, ratingname = self.df.keys()[sessioncolumn-1], self.df.keys()[ratingcolumn-1]
            sessionval, ratingval = self.df[sessionname].to_numpy(), self.df[ratingname].to_numpy()
            sessionnum = CH_Automation.uniquevalcount(self, self.name, sessioncolumn, rows)
            uniqsessions = {}
            uniq = np.unique((self.df[sessionname].dropna(how = 'all')).to_numpy())
        for session in uniq:
            uniqsessions[session] = 0
        for i in range(len(sessionval)):
            for session in uniqsessions:
                if sessionval[i] == session:
                    if pd.notna(ratingval[i]):
                        uniqsessions[session] += int(str(ratingval[i])[0])
        return uniqsessions, sessionnum
    
    def totalsessionratings(self, sessioncolumn, ratingcolumn, rows = None, sort = None):
        sessionnum = {}
        if len(sessioncolumn) == len(ratingcolumn) and list in (type(sessioncolumn), type(ratingcolumn)):    
            for i in range(len(sessioncolumn)):
                if i == 0:
                    ratingnum = self.sessionratings(sessioncolumn[0], ratingcolumn[0], rows, sort)[0]
                else:
                    ratingnum.update(self.sessionratings(sessioncolumn[i], ratingcolumn[i], rows, sort)[0])
            for session in ratingnum:
                ratingnum[session] = 0
                sessionnum[session] = 0
            for i in range(len(sessioncolumn)):
                rating, sessions = self.sessionratings(sessioncolumn[i], ratingcolumn[i], rows, sort)
                for session in ratingnum:
                    try:
                        ratingnum[session] += int(rating[session])
                        sessionnum[session] += int(sessions[session])
                    except:
                        None
            for session in ratingnum:
                ratingnum[session] = round(ratingnum[session]/sessionnum[session], 2)
            return ratingnum
        else:
            raise ValueError
    
    def siteratings(self, sitename, sitecolumn, sessioncolumn, ratingcolumn):
        sites, siterange = CH_Automation.columnrange(self, self.name, sitecolumn), []
        for i in sites:
            if i == sitename:
                siterange = sites[i]
        return self.totalsessionratings(sessioncolumn, ratingcolumn, siterange, sort = True)
    
    def bargraph(self, sessioncolumn, ratingcolumn):
        data = self.totalsessionratings(sessioncolumn, ratingcolumn)
        sessions = list(data.keys())
        ratings = list(data.values())
        plt.bar(sessions, ratings)
        plt.title('Session Ratings')
    
    def sitebargraph(self, sitename, sitecolumn, sessioncolumn, ratingcolumn):
        data = self.siteratings(sitename, sitecolumn, sessioncolumn, ratingcolumn)
        sessions = list(data.keys())
        ratings = list(data.values())
        plt.bar(sessions, ratings)
        plt.title('Site Session Ratings')
        
    def externattendance(self, externname, namecolumn, sitecolumn, sessioncolumn):
        namecolumnname, sitecolumnname = self.df.keys()[namecolumn-1], self.df.keys()[sitecolumn-1]
        attendance = []
        for i in range(len(self.df[namecolumnname])):
            if self.df[namecolumnname][i] == externname:
                sitename = self.df[sitecolumnname][i]
        sites, siterange = CH_Automation.columnrange(self, self.name, sitecolumn), []
        for i in sites:
            if i == sitename:
                siterange = sites[i]
        for i in range(siterange[0], siterange[1]+1):
            if externname == self.df.to_numpy()[i][namecolumn-1]:
                for j in range(len(sessioncolumn)):
                    if pd.notna(self.df.to_numpy()[i][sessioncolumn[j]-1]):
                        attendance.append(self.df.to_numpy()[i][sessioncolumn[j]-1])
        attendance = np.unique(np.array(attendance))
        sitesessions = []
        for i in range(siterange[0], siterange[1]+1):
            for j in range(len(sessioncolumn)):
                sitesessions.append(self.df.to_numpy()[i][sessioncolumn[j]-1])
        sitesessions = (np.unique(np.array(sitesessions))).tolist()
        for sessions in sitesessions:
            for externsessions in attendance:
                if sessions == externsessions:
                    sitesessions.remove(sessions)
        return sitesessions

c = Demographics(r"C:\Users\jasoli3\Downloads\2022 Extern Details.xlsx")

