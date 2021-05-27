# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Props(models.Model):
    Name = models.TextField(db_column='Name', primary_key=True)
    Length = models.FloatField(db_column='Length', blank=True, null=True)
    Mass = models.FloatField(db_column='Mass', blank=True, null=True)
    SASAmiller = models.FloatField(db_column='SASAmiller', blank=True, null=True)
    NetCh = models.FloatField(db_column='NetCh', blank=True, null=True)
    NCD = models.FloatField(db_column='NCD', blank=True, null=True)
    fFatty = models.FloatField(db_column='fFatty', blank=True, null=True)
    fPos = models.FloatField(db_column='fPos', blank=True, null=True)
    fNeg = models.FloatField(db_column='fNeg', blank=True, null=True)
    GC = models.FloatField(db_column='GC', blank=True, null=True)
    seqnum = models.FloatField(db_column='SeqNum', blank=True, null=True)
    fCharged = models.FloatField(db_column='fCharged', blank=True, null=True)
    ncd1000 = models.FloatField(db_column='NCD1000', blank=True, null=True)
    mwkda = models.FloatField(db_column='MWkDa', blank=True, null=True)
    i = models.FloatField(db_column='I', blank=True, null=True)
    l = models.FloatField(db_column='L', blank=True, null=True)
    v = models.FloatField(db_column='V', blank=True, null=True)
    a = models.FloatField(db_column='A', blank=True, null=True)
    g = models.FloatField(db_column='G', blank=True, null=True)
    p = models.FloatField(db_column='P', blank=True, null=True)
    f = models.FloatField(db_column='F', blank=True, null=True)
    m = models.FloatField(db_column='M', blank=True, null=True)
    w = models.FloatField(db_column='W', blank=True, null=True)
    y = models.FloatField(db_column='Y', blank=True, null=True)
    h = models.FloatField(db_column='H', blank=True, null=True)
    t = models.FloatField(db_column='T', blank=True, null=True)
    s = models.FloatField(db_column='S', blank=True, null=True)
    n = models.FloatField(db_column='N', blank=True, null=True)
    q = models.FloatField(db_column='Q', blank=True, null=True)
    d = models.FloatField(db_column='D', blank=True, null=True)
    e = models.FloatField(db_column='E', blank=True, null=True)
    k = models.FloatField(db_column='K', blank=True, null=True)
    r = models.FloatField(db_column='R', blank=True, null=True)
    c = models.FloatField(db_column='C', blank=True, null=True)
    x = models.FloatField(db_column='X', blank=True, null=True)
    u = models.FloatField(db_column='U', blank=True, null=True)
    kingdom = models.TextField(blank=True, null=True)
    phylum = models.TextField(blank=True, null=True)
    taxClass = models.TextField(db_column='class', blank=True, null=True)
    order = models.TextField(blank=True, null=True)
    family = models.TextField(blank=True, null=True)
    genus = models.TextField(blank=True, null=True)
    species = models.TextField(db_column='Species', blank=True, null=True)
    taxid = models.TextField(db_column='Taxid', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Props'

    def __str__(self):
        return f"{self.Name}; {self.species} ({self.kingdom})"

    def serialize(self):
        """Dictionary representation of properties"""
        result = dict()
        for field_name in [field.name for field in self._meta.fields]:
            result.update( {field_name : self.__dict__[field_name]} )

        return result
